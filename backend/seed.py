"""
Database seeding script
Creates demo departments, users, and documents
"""
import sys
from pathlib import Path
from sqlalchemy.orm import Session

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models.base import Base
import app.models
from app.models.department import Department
from app.models.user import User
from app.models.document import Document
from app.services.rag_service import rag_service

def seed_departments(db: Session):
    """Seed 5 departments."""
    departments = [
        {"name": "Human Resources", "code": "HR", "description": "Leave, attendance, employee records"},
        {"name": "Finance", "code": "FINANCE", "description": "Salary, reimbursements, tax"},
        {"name": "Information Technology", "code": "IT", "description": "System access, hardware, software support"},
        {"name": "Pension", "code": "PENSION", "description": "Retirement benefits, pension queries"},
        {"name": "Administration", "code": "ADMIN", "description": "Office management, facilities"}
    ]
    
    created_depts = []
    for dept_data in departments:
        existing = db.query(Department).filter(Department.code == dept_data["code"]).first()
        if not existing:
            dept = Department(**dept_data)
            db.add(dept)
            created_depts.append(dept)
        else:
            created_depts.append(existing)
    
    db.commit()
    print(f"✅ Seeded {len(departments)} departments")
    return created_depts

def seed_users(db: Session, departments):
    """Seed demo users for all 4 roles."""
    demo_pwd = "Demo@1234"
    users_data = [
        # Super Admin
        {
            "email": "superadmin@demo.gov.in",
            "password": demo_pwd,
            "full_name": "Super Administrator",
            "employee_id": "SA001",
            "role": "SuperAdmin",
            "department_id": None
        },
        # Department Admins (one per department)
        {
            "email": "admin.hr@demo.gov.in",
            "password": demo_pwd,
            "full_name": "HR Admin",
            "employee_id": "HRA001",
            "role": "DeptAdmin",
            "department_id": departments[0].id
        },
        {
            "email": "admin.finance@demo.gov.in",
            "password": demo_pwd,
            "full_name": "Finance Admin",
            "employee_id": "FINA001",
            "role": "DeptAdmin",
            "department_id": departments[1].id
        },
        # Department Officers
        {
            "email": "officer.hr@demo.gov.in",
            "password": demo_pwd,
            "full_name": "HR Officer",
            "employee_id": "HRO001",
            "role": "Officer",
            "department_id": departments[0].id
        },
        {
            "email": "officer.it@demo.gov.in",
            "password": demo_pwd,
            "full_name": "IT Support Officer",
            "employee_id": "ITO001",
            "role": "Officer",
            "department_id": departments[2].id
        },
        # Employees
        {
            "email": "employee@demo.gov.in",
            "password": demo_pwd,
            "full_name": "John Employee",
            "employee_id": "EMP001",
            "role": "Employee",
            "department_id": departments[0].id
        },
        {
            "email": "rajesh.kumar@demo.gov.in",
            "password": demo_pwd,
            "full_name": "Rajesh Kumar",
            "employee_id": "EMP002",
            "role": "Employee",
            "department_id": departments[1].id
        }
    ]
    
    created_users = []
    for user_data in users_data:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        password = user_data.pop("password")
        if not existing:
            user = User(**user_data, hashed_password=get_password_hash(password))
            db.add(user)
            created_users.append(user)
        else:
            existing.hashed_password = get_password_hash(password)
            created_users.append(existing)
    
    db.commit()
    print(f"✅ Seeded {len(users_data)} users")
    return created_users

def create_demo_documents():
    """Create demo document files in demo-data directory."""
    demo_data_dir = Path(__file__).parent.parent / "demo-data"
    demo_data_dir.mkdir(exist_ok=True)
    
    documents = {
        "HR": [
            ("leave_policy.txt", """LEAVE POLICY - GOVERNMENT OF INDIA (Demo Document)

Casual Leave (CL):
- Employees are entitled to 8 days of Casual Leave per year
- CL can be taken for a maximum of 5 consecutive days
- Apply at least 2 days in advance through the online portal
- Unused CL cannot be carried forward

Earned Leave (EL):
- 30 days per year
- Can be accumulated up to 300 days
- Encashment available on retirement
- Apply 15 days in advance for leave exceeding 10 days

Medical Leave:
- Half-pay leave: 20 days per year
- Commuted leave: Up to 90 days during entire service
- Medical certificate required for leaves exceeding 5 days

Maternity Leave:
- 180 days (6 months) for female employees
- Can be availed 8 weeks before expected delivery date
- Submit medical certificate from registered practitioner"""),
            
            ("attendance_system.txt", """BIOMETRIC ATTENDANCE SYSTEM - USER GUIDE

System Login:
- Use your employee ID and password at http://attendance.gov.in
- First-time users: Default password is your date of birth (DDMMYYYY)
- Change password immediately after first login

Daily Attendance:
- Office hours: 9:30 AM to 6:00 PM
- Grace time: 15 minutes
- Late arrivals (after 9:45 AM) require supervisor approval
- Minimum working hours per day: 8 hours (excluding lunch break)

Regularization:
- Missed biometric punch: Apply for regularization within 3 days
- Attach supporting documents (medical certificate, travel proof, etc.)
- Approval required from reporting officer

Monthly Reports:
- View your attendance report from Dashboard → My Attendance
- Download monthly reports for reimbursement claims
- Discrepancies should be reported to HR within 5 days of month end"""),
            
            ("transfer_procedure.txt", """INTER-DEPARTMENT TRANSFER PROCEDURE

Eligibility:
- Minimum 2 years of service in current department
- No pending disciplinary action
- Performance rating: Good or above

Application Process:
1. Fill Form T-101 available on employee portal
2. Obtain NOC from current Head of Department
3. Submit to Establishment Section with:
   - Last 2 years' performance appraisals
   - Recommendation letter from reporting officer
   - Reason for transfer (personal/official)

Processing Time:
- Normal transfer: 60-90 days
- On medical grounds: 30-45 days (attach medical certificate)
- Spouse transfer: Priority processing (45 days)

Approval Authority:
- Within same ministry: Joint Secretary
- Between ministries: Cabinet approval required""")
        ],
        
        "FINANCE": [
            ("expense_reimbursement.txt", """EXPENSE REIMBURSEMENT POLICY (Demo)

Travel Reimbursement:
- Local travel (within city): Actual bus/metro fare or ₹500/day (whichever lower)
- Outstation travel: As per entitlement (Air/Train based on grade)
- Submit claims within 30 days of travel completion
- Required documents: Tickets, boarding passes, hotel bills

Medical Reimbursement:
- Maximum limit: ₹5000 per month or actual (whichever lower)
- CGHS beneficiaries: Follow CGHS procedures
- Non-CGHS: Submit original bills with prescription
- Emergency treatment: Inform HR within 48 hours

Telephone/Internet:
- Grade A & above: ₹2000/month
- Grade B: ₹1500/month
- Submit itemized bill with payment proof
- Personal calls not reimbursable

Processing Timeline:
- Complete application with all documents: 15 working days
- Incomplete application: Return for correction within 7 days
- Payment: Direct bank transfer by 7th of following month"""),
            
            ("salary_components.txt", """SALARY STRUCTURE - CENTRAL GOVERNMENT EMPLOYEES

Basic Pay:
- 7th Pay Commission matrix
- Annual increment: 3% (every July)
- Stagnation increment after maximum scale

Allowances:
- Dearness Allowance (DA): Current rate 42% of Basic Pay (revised quarterly)
- House Rent Allowance (HRA):
  * X-class cities: 24% of Basic
  * Y-class cities: 16% of Basic
  * Z-class cities: 8% of Basic
- Transport Allowance: ₹3600 + DA

Deductions:
- Income Tax (as per IT slab)
- Provident Fund (GPF): 6% of Basic + DA (minimum)
- Professional Tax: ₹200/month (state-dependent)
- Group Insurance: ₹120/month

Bonus & Incentives:
- Performance-linked bonus: Up to 20% of Basic Pay
- Productivity-linked bonus: ₹3500 annually
- Festival advance: ₹10,000 (non-interest bearing)

Salary Slip:
- Available on HRMS portal by 25th of every month
- Download and save for tax filing
- Discrepancies: Report to Accounts Section within 5 days"""),
            
            ("tax_declaration.txt", """INCOME TAX DECLARATION - ANNUAL PROCESS

Investment Declaration (Before Start of FY):
- Submit Form 12BB by May 31st
- Declare planned investments under Section 80C (up to ₹1.5 lakh)
- Medical insurance premium: Section 80D
- Home loan interest: Section 24

Proof Submission (End of FY):
- Deadline: February 28th of assessment year
- Accepted proofs:
  * PPF passbook copy
  * LIC premium receipt
  * Home loan certificate from bank
  * Tuition fee receipt (2 children max)
  * National Savings Certificate

Form 16:
- Issued by May 31st annually
- Download from HRMS portal
- Contains TDS deducted by employer
- Use for filing IT return

Reimbursement of TDS:
- If excess TDS deducted: File revised return
- Refund processed by Income Tax Department (not employer)
- Update PAN and bank details in HRMS""")
        ],
        
        "IT": [
            ("email_account_setup.txt", """OFFICIAL EMAIL ACCOUNT - SETUP GUIDE

Account Creation:
- All employees receive: firstname.lastname@gov.in
- Credentials sent to personal email within 3 working days of joining
- Default password: Sent via SMS to registered mobile

Email Client Configuration:
- Webmail: https://mail.gov.in
- IMAP Settings:
  * Server: imap.gov.in
  * Port: 993 (SSL enabled)
- SMTP Settings:
  * Server: smtp.gov.in
  * Port: 587 (TLS)

Mobile Device Setup:
- Android: Use Gmail app with "Other" account option
- iOS: Mail app → Add Account → IMAP
- Two-factor authentication required for mobile access

Storage & Quotas:
- Mailbox size: 10 GB per user
- Attachment limit: 25 MB per email
- Archive old emails to local storage quarterly

Security Guidelines:
- Change password every 90 days
- Do not share credentials
- Report phishing emails to it.helpdesk@gov.in
- Use encryption for sensitive data"""),
            
            ("vpn_access.txt", """VPN ACCESS FOR REMOTE WORK

Eligibility:
- Permanent employees (minimum 6 months service)
- Approved by Head of Department
- Signed remote work agreement

VPN Client Installation:
1. Download "Gov-Secure VPN" from IT portal
2. Install with administrator privileges
3. Generate certificate from https://vpn.gov.in using employee ID
4. Import certificate into VPN client

Connection Steps:
- Open Gov-Secure VPN client
- Enter employee ID and password
- Enter OTP sent to registered mobile
- Click "Connect" - Status should show "Connected"

Permitted Usage:
- Access to internal file servers
- HRMS and other internal applications
- Official email (already accessible without VPN)
- Working hours: 8 AM to 8 PM (extended access requires approval)

Troubleshooting:
- Connection failed: Check internet connectivity
- Certificate expired: Regenerate from portal (valid 90 days)
- OTP not received: Contact IT helpdesk
- Helpdesk: 1800-XXX-XXXX (Mon-Fri, 9 AM - 6 PM)"""),
            
            ("password_reset.txt", """PASSWORD RESET PROCEDURE

Self-Service Password Reset:
1. Visit https://password.gov.in
2. Click "Forgot Password"
3. Enter employee ID or email
4. Answer security questions (set during account creation)
5. Enter OTP sent to registered mobile
6. Set new password (min 12 characters, mix of upper/lower/numbers/symbols)

Helpdesk Assisted Reset:
- Call IT Helpdesk: 1800-XXX-XXXX
- Verify identity: Employee ID, Date of Birth, Department
- Temporary password sent to official email
- Must change temporary password on first login

Password Policy:
- Length: Minimum 12 characters
- Complexity: At least 1 uppercase, 1 lowercase, 1 number, 1 special character
- Expiry: 90 days (notification 7 days before expiry)
- History: Cannot reuse last 5 passwords
- Account lockout: After 5 failed attempts (unlocks after 30 minutes)

Security Tips:
- Never write down passwords
- Do not share with colleagues
- Use different passwords for different systems
- Enable two-factor authentication where available""")
        ],
        
        "PENSION": [
            ("pension_eligibility.txt", """PENSION ELIGIBILITY - CENTRAL GOVERNMENT

Service Requirements:
- Minimum qualifying service: 10 years
- Voluntary retirement: After 20 years of service
- Superannuation: Age 60 years
- Medical retirement: Based on Medical Board recommendation

Types of Pension:
1. Service Pension:
   - 50% of last drawn basic pay (average of last 10 months)
   - Minimum pension: ₹9000/month
   - Dearness Relief applicable (at same rate as DA for serving employees)

2. Family Pension:
   - Payable to spouse/dependent children after employee death
   - Normal rate: 30% of basic pay
   - Enhanced rate: 50% of basic pay for first 7 years (if death in service)

3. Disability Pension:
   - 100% medical disability: 100% of pension admissible
   - Less than 100%: Proportionate pension based on disability percentage

Commutation of Pension:
- Maximum 40% of pension can be commuted
- Lump sum payment = 40% × pension × commutation factor (based on age)
- Commuted portion restored after 15 years

Application Process:
- Submit Form 1 (pension application) 6 months before retirement
- Attend pre-retirement counseling (mandatory)
- Update family details, bank account, nomination"""),
            
            ("gpf_withdrawal.txt", """GENERAL PROVIDENT FUND (GPF) - WITHDRAWAL RULES

GPF Account:
- Mandatory for all permanent employees
- Minimum contribution: 6% of Basic + DA
- Interest rate: Revised quarterly (current: 7.1% p.a.)

Part Withdrawal (While in Service):
Allowed for:
- Construction/purchase of house (up to 90% of GPF balance)
- Children's education (up to 50%)
- Medical treatment (up to 90%)
- Marriage (self/children) - up to 50%

Conditions:
- Minimum 5 years of GPF subscription
- Maximum 3 withdrawals in entire service
- Repayment not required (but reduces final balance)

Application Procedure:
1. Fill Form GPF-3 (available on HRMS portal)
2. Attach supporting documents (quotation/admission letter/medical bill)
3. Submit to Accounts Section
4. Approval by competent authority
5. Payment: Within 30 days of approval

Final Withdrawal (On Retirement):
- Submit Form GPF-5 along with pension papers
- Entire balance + interest payable
- Payment within 90 days of retirement
- Bank account details must be updated

Nominee Update:
- Update Form GPF-1 every 5 years or on family status change
- Nominee can claim GPF in case of employee death
- Joint declaration by employee and nominee required"""),
            
            ("retirement_checklist.txt", """PRE-RETIREMENT CHECKLIST

6 Months Before Retirement:
☐ Attend pre-retirement counseling session (mandatory)
☐ Submit Form 1 (Pension application)
☐ Update service book and get verified
☐ Apply for GPF final withdrawal
☐ Update family details, nominee, bank account

3 Months Before:
☐ Apply for gratuity (Form 14)
☐ Commutation application (if opting)
☐ Apply for Leave Encashment
☐ Submit LTC claims (if any pending)
☐ Medical check-up for CS(MA) benefits

1 Month Before:
☐ No-dues certificate from:
  - Library
  - Finance (advance clearance)
  - IT (laptop, phone return)
  - Admin (office keys, vehicle)
☐ Return official identity card
☐ Apply for pension payment order (PPO)
☐ Open savings account (if not existing) for pension credit

After Retirement:
☐ Collect Pension Payment Order (PPO)
☐ Submit life certificate every November (for pension continuity)
☐ Register for Pensioners' Portal (for grievances)
☐ Update address/bank changes immediately

Important Contacts:
- Pension Cell: pension@gov.in, 011-XXXX-XXXX
- GPF Section: gpf@gov.in
- Gratuity: gratuity@gov.in""")
        ],
        
        "ADMIN": [
            ("office_timings.txt", """OFFICE TIMINGS AND ATTENDANCE

Standard Working Hours:
- Monday to Friday: 9:30 AM to 6:00 PM
- Lunch break: 1:00 PM to 1:30 PM (30 minutes)
- Saturday: 2nd and 4th Saturday working (9:30 AM to 2:00 PM)
- Total weekly hours: 42.5 hours

Flexible Timing:
- Available for Grade B and above (subject to HOD approval)
- Core hours (mandatory): 11:00 AM to 4:00 PM
- Flexi window: 8:30 AM to 10:30 AM (arrival), 5:00 PM to 7:00 PM (departure)
- Minimum 8 hours per day mandatory

Late Coming:
- Grace period: 15 minutes (3 times per month)
- Beyond grace: Half-day casual leave
- Repeated late coming: Disciplinary action

Early Departure:
- Requires prior approval from reporting officer
- Apply via HRMS → Leave → Permission for early departure
- Maximum 2 hours early (counted as short leave)

Attendance Regularization:
- Missed biometric punch: Apply within 3 days
- Attach supporting document (if applicable)
- Approval: First level - Reporting Officer, Second level - HR

Remote Work:
- Allowed maximum 2 days per week (post-pandemic policy)
- Prior approval required
- Applicable only for roles identified by department
- Full-day deliverables mandatory"""),
            
            ("visitor_management.txt", """VISITOR MANAGEMENT SYSTEM

Visitor Entry:
- All visitors must register at Reception (Gate 1)
- Valid photo ID mandatory (Aadhaar/Driving License/Passport)
- Visitor pass issued after host employee confirmation
- Entry time: 9:00 AM to 5:30 PM (Monday-Friday)

Visitor Pass Types:
1. Single-day pass: Valid till 6:00 PM same day
2. Multiple-day pass: Requires HOD approval (max 5 days)
3. Contractor pass: Valid for contract duration (with photo)

Host Employee Responsibilities:
- Must confirm visitor via SMS/email to reception
- Meet visitor at reception within 15 minutes
- Ensure visitor wears pass visibly
- Escort visitor at all times in restricted areas
- Return pass at departure

Meeting Room Booking:
- Book via Facility Portal: https://facility.gov.in
- Conference Room A (capacity 50): Requires 7 days advance booking
- Meeting Rooms B, C, D (capacity 10-15): 2 days advance
- Cancellation: At least 4 hours before scheduled time
- Facilities: Projector, Video conferencing (on request)

VIP Visitors:
- Inform Admin Section 3 days in advance
- Provide: Name, designation, expected time, purpose
- Security clearance processed by Security Officer
- Parking reserved in VIP zone

Security Restrictions:
- Laptops/cameras: Prior approval from Security
- Mobile phones allowed in general areas
- Restricted zones: No photography
- Unattended baggage: Immediately report to security"""),
            
            ("vehicle_parking.txt", """PARKING AND VEHICLE MANAGEMENT

Parking Allocation:
- Grade A and above: Reserved parking (car)
- Grade B: General parking (car/two-wheeler)
- Grade C and below: Two-wheeler parking
- Contract staff: Designated zone near Gate 2

Vehicle Registration:
1. Submit application to Admin Section (Form V-101)
2. Attach: Vehicle RC copy, insurance, pollution certificate
3. Parking sticker issued (display on windshield)
4. Annual renewal required (before March 31)

Parking Rules:
- Park only in allocated slot/zone
- Speed limit inside campus: 20 km/h
- No parking in fire lane, entrances, or visitor zones
- Violation: Warning (1st), Fine ₹500 (2nd), Sticker cancellation (3rd)

Two-Wheeler Parking:
- Helmet mandatory (even inside campus)
- Use parking stand
- Chain-locking encouraged

Electric Vehicle (EV) Charging:
- 4 charging points available in Block A parking
- Free charging for government vehicles
- Prior slot booking: evcharging@gov.in
- Charging time: Maximum 2 hours per vehicle

Visitor Parking:
- Limited slots (first-come-first-served)
- Register vehicle at Gate 1
- Time limit: 3 hours
- Overflow parking: Public parking 200m from Gate 3

Cycle Stand:
- Available near all blocks
- Covered parking
- Bicycle allowance: ₹500/month (on proof of usage)

Important:
- Do not leave valuables in vehicle
- Report accidents inside campus to Security immediately
- Toll/parking receipts: Not reimbursable for personal vehicles""")
        ]
    }
    
    for dept_code, files in documents.items():
        dept_dir = demo_data_dir / dept_code
        dept_dir.mkdir(exist_ok=True)
        
        for filename, content in files:
            file_path = dept_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"✅ Created demo documents in {demo_data_dir}")
    return demo_data_dir

def seed_documents(db: Session, departments, demo_data_dir: Path):
    """Seed documents and ingest into RAG."""
    dept_map = {dept.code: dept for dept in departments}
    admin_user = db.query(User).filter(User.role == "SuperAdmin").first()
    
    count = 0
    for dept_code, dept in dept_map.items():
        dept_dir = demo_data_dir / dept_code
        if not dept_dir.exists():
            continue
        
        for file_path in dept_dir.glob("*.txt"):
            # Check if already exists
            existing = db.query(Document).filter(
                Document.filename == file_path.name,
                Document.department_id == dept.id
            ).first()
            
            if not existing:
                doc = Document(
                    title=file_path.stem.replace('_', ' ').title(),
                    filename=file_path.name,
                    file_path=str(file_path),
                    file_type="txt",
                    file_size=file_path.stat().st_size,
                    department_id=dept.id,
                    uploaded_by=admin_user.id,
                    description=f"Demo document for {dept.name}"
                )
                db.add(doc)
                db.commit()
                db.refresh(doc)
            else:
                doc = existing
            
            # Ingest into RAG
            try:
                num_chunks = rag_service.ingest_document(
                    document_id=doc.id,
                    department_id=dept.id,
                    file_path=str(file_path),
                    title=doc.title,
                    file_type="txt"
                )
                print(f"  📄 {doc.title} ({dept_code}): {num_chunks} chunks")
                count += 1
            except Exception as e:
                print(f"  ⚠️  Failed to ingest {doc.title}: {e}")
    
    print(f"✅ Seeded and ingested {count} documents into RAG")

def main():
    print("🌱 Starting database seeding...\n")
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Seed in order
        departments = seed_departments(db)
        users = seed_users(db, departments)
        demo_data_dir = create_demo_documents()
        seed_documents(db, departments, demo_data_dir)
        
        print("\n" + "="*60)
        print("🎉 SEEDING COMPLETE!")
        print("="*60)
        print("\n📧 Demo Login Credentials:")
        print("-" * 60)
        print("Super Admin:     superadmin@demo.gov.in / super123")
        print("Dept Admin (HR): admin.hr@demo.gov.in / admin123")
        print("Officer (HR):    officer.hr@demo.gov.in / officer123")
        print("Employee:        employee@demo.gov.in / employee123")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()