"""
Migration script to import existing Markdown rules into database

Run this script to migrate from file-based rules to database-based rules.
Usage: python -m backend.scripts.migrate_rules
"""
import asyncio
import sys
import re
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from database import AsyncSessionLocal, init_db
from models import ChecklistCategory, QuestionType
import crud_rules
import crud


def parse_checklist_markdown(filepath: str, category: str) -> list:
    """Parse a checklist markdown file and extract items"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        items = []
        display_order = 0
        
        # Split by main headings (###)
        sections = re.split(r'\n### ', content)
        
        for section in sections[1:]:  # Skip first split (header)
            lines = section.split('\n')
            if not lines:
                continue
            
            # Extract item number and title from first line
            first_line = lines[0].strip()
            match = re.match(r'^(\d+[a-z]?)\.\s+(.+)$', first_line)
            
            if not match:
                continue
            
            item_number = match.group(1)
            title = match.group(2)
            
            # Extract description, required docs, and notes
            description_parts = []
            required_documents = []
            notes = []
            
            current_section = "description"
            i = 1
            
            while i < len(lines):
                line = lines[i].strip()
                
                if not line or line.startswith('#'):
                    i += 1
                    continue
                
                # Check for checkbox items
                if line.startswith('- [ ]'):
                    # This is the main item description
                    desc = line.replace('- [ ]', '').strip().strip('**')
                    if desc:
                        description_parts.append(desc)
                elif line.startswith('  - '):
                    # Sub-bullet points
                    sub_item = line.strip()[2:].strip()
                    if sub_item.startswith('Description:'):
                        description_parts.append(sub_item.replace('Description:', '').strip())
                    elif sub_item.startswith('Why it\'s needed:') or sub_item.startswith('Why it's needed:'):
                        pass  # Skip for brevity
                    elif sub_item.startswith('What to provide:'):
                        current_section = "documents"
                    elif sub_item.startswith('Examples:') or sub_item.startswith('Key requirements:'):
                        current_section = "notes"
                    elif sub_item.startswith('⚠️') or sub_item.startswith('🟢'):
                        notes.append(sub_item)
                    elif current_section == "documents":
                        required_documents.append(sub_item)
                    elif current_section == "notes":
                        notes.append(sub_item)
                    else:
                        description_parts.append(sub_item)
                
                i += 1
            
            items.append({
                "category": category,
                "item_number": item_number,
                "title": title,
                "description": ' '.join(description_parts) if description_parts else None,
                "required_documents": '\n'.join(required_documents) if required_documents else None,
                "notes": '\n'.join(notes) if notes else None,
                "is_active": True,
                "display_order": display_order
            })
            
            display_order += 1
        
        return items
    
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return []


async def migrate_checklist_items(db):
    """Migrate checklist items from markdown files"""
    print("\n=== Migrating Checklist Items ===")
    
    backend_path = Path(__file__).parent.parent
    
    # Parse DPA checklist
    dpa_file = backend_path / "knowledge" / "dpa_checklist.md"
    if dpa_file.exists():
        print(f"Parsing {dpa_file}...")
        dpa_items = parse_checklist_markdown(str(dpa_file), "DPA")
        print(f"Found {len(dpa_items)} DPA checklist items")
        
        for item in dpa_items:
            try:
                await crud_rules.create_checklist_item(db, item, user_id=None)
                print(f"  ✓ Imported: {item['item_number']}. {item['title'][:50]}...")
            except Exception as e:
                print(f"  ✗ Error importing {item['item_number']}: {e}")
    
    # Parse OTIA checklist
    otia_file = backend_path / "knowledge" / "otia_checklist.md"
    if otia_file.exists():
        print(f"\nParsing {otia_file}...")
        otia_items = parse_checklist_markdown(str(otia_file), "OTIA")
        print(f"Found {len(otia_items)} OTIA checklist items")
        
        for item in otia_items:
            try:
                await crud_rules.create_checklist_item(db, item, user_id=None)
                print(f"  ✓ Imported: {item['item_number']}. {item['title'][:50]}...")
            except Exception as e:
                print(f"  ✗ Error importing {item['item_number']}: {e}")


async def migrate_screening_questions(db):
    """Migrate screening questions from agent config"""
    print("\n=== Migrating Screening Questions ===")
    
    # Get default screening questions from agent config
    config = await crud.get_agent_config(db)
    
    if config and "screening_questions" in config:
        questions = config["screening_questions"]
        print(f"Found {len(questions)} screening questions")
        
        for i, question_text in enumerate(questions):
            try:
                question_data = {
                    "question_text": question_text,
                    "question_type": "yes_no",
                    "is_active": True,
                    "display_order": i
                }
                await crud_rules.create_screening_question(db, question_data, user_id=None)
                print(f"  ✓ Imported: {question_text[:60]}...")
            except Exception as e:
                print(f"  ✗ Error importing question: {e}")
    else:
        print("No screening questions found in agent config")


async def migrate_sensitive_keywords(db):
    """Migrate sensitive keywords from agent config"""
    print("\n=== Migrating Sensitive Keywords ===")
    
    # Get default keywords from agent config
    config = await crud.get_agent_config(db)
    
    if config and "sensitive_data_keywords" in config:
        keywords = config["sensitive_data_keywords"]
        print(f"Found {len(keywords)} sensitive keywords")
        
        # Categorize keywords
        financial_keywords = ["credit score", "transaction", "BNPL", "loan", "payment", "bank account", "salary", "income"]
        health_keywords = ["health", "biometric"]
        
        for keyword in keywords:
            try:
                # Determine category
                if keyword.lower() in [k.lower() for k in financial_keywords]:
                    category = "financial"
                elif keyword.lower() in [k.lower() for k in health_keywords]:
                    category = "health"
                else:
                    category = "general"
                
                keyword_data = {
                    "keyword": keyword,
                    "category": category,
                    "is_active": True
                }
                await crud_rules.create_sensitive_keyword(db, keyword_data, user_id=None)
                print(f"  ✓ Imported: {keyword} ({category})")
            except Exception as e:
                print(f"  ✗ Error importing keyword '{keyword}': {e}")
    else:
        print("No sensitive keywords found in agent config")


async def main():
    """Main migration function"""
    print("=" * 60)
    print("Data Privacy Intake Agent - Rules Migration Script")
    print("=" * 60)
    print("\nThis script will import existing rules from Markdown files")
    print("and agent config into the database.")
    print("\nIMPORTANT: This will create NEW records. Run only once!")
    print("\n" + "=" * 60)
    
    # Wait for user confirmation
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Migration cancelled.")
        return
    
    # Initialize database
    print("\nInitializing database...")
    await init_db()
    
    # Run migrations
    async with AsyncSessionLocal() as db:
        try:
            # Ensure default admin and config exist
            await crud.init_default_user(db)
            await crud.init_default_agent_config(db)
            await crud.init_default_settings(db)
            await db.commit()
            
            # Migrate data
            await migrate_checklist_items(db)
            await migrate_screening_questions(db)
            await migrate_sensitive_keywords(db)
            
            await db.commit()
            
            print("\n" + "=" * 60)
            print("✓ Migration completed successfully!")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Review imported rules in the Admin Panel")
            print("2. Adjust display order if needed")
            print("3. Add/edit/delete rules as necessary")
            print("\nDefault admin credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  (Please change the password after first login!)")
            
        except Exception as e:
            print(f"\n✗ Migration failed: {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
