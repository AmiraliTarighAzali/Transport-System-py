# setup.py
import os

def create_structure():
    print("🚀 Creating Transport System Project Structure...")
    
    # ساختار پوشه‌ها
    directories = [
        'src/admin',
        'src/employee',
        'src/user', 
        'src/wallet',
        'src/shared',
        'data',
        'docs',
        'tests'
    ]
    
    # ساخت فولدرها
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created: {directory}")
    
    # لیست فایل‌ها
    files = [
        'src/main.py',
        'src/__init__.py',
        'requirements.txt',
        'BANK.py',
        'README.md',
        '.gitignore',
        'github_link.txt',
        
        # بخش admin
        'src/admin/__init__.py',
        'src/admin/admin_panel.py',
        'src/admin/employee_manager.py',
        
        # بخش employee
        'src/employee/__init__.py',
        'src/employee/employee_panel.py',
        'src/employee/line_manager.py',
        'src/employee/train_manager.py',
        
        # بخش user
        'src/user/__init__.py',
        'src/user/user_panel.py',
        'src/user/registration.py',
        'src/user/profile_manager.py',
        
        # بخش wallet
        'src/wallet/__init__.py',
        'src/wallet/wallet_manager.py',
        'src/wallet/payment_handler.py',
        'src/wallet/transaction_logger.py',
        
        # بخش shared
        'src/shared/__init__.py',
        'src/shared/validators.py',
        'src/shared/data_structures.py',
        'src/shared/auth.py',
        'src/shared/utils.py',
        
        # مستندات
        'docs/project_flowchart.md',
        'docs/team_division.md',
        'docs/requirements.md'
    ]
    
    # ساخت فایل‌ها
    for file in files:
        with open(file, 'w', encoding='utf-8') as f:
            # اضافه کردن محتوای اولیه برای بعضی فایل‌ها
            if file == 'README.md':
                f.write("# 🚆 Transport System Project\n\nQBC11 Bootcamp Project 1\n")
            elif file == '.gitignore':
                f.write("__pycache__/\n*.pyc\nvenv/\n.env\n*.log\n")
            elif file == 'requirements.txt':
                f.write("# Python Dependencies\n")
        print(f"📄 Created: {file}")
    
    print("\n✅ Project structure created successfully!")
    print("📦 Next steps:")
    print("   1. Run: git add .")
    print("   2. Run: git commit -m 'Initial project structure'")
    print("   3. Run: git push origin main")

if __name__ == "__main__":
    create_structure()