cd coficheckout


Create a virtual environment and activate

python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

Install Django
pip install django

Run Django migrations

python manage.py makemigrations
python manage.py migrate


Start the server

python manage.py runserver


Open the app in your browser

http://127.0.0.1:8000/

Usage

Select the quantity for each product.

Click Check Available Discounts to see eligible discounts.

Check any available discount to see its description.

Click Apply Discounts to calculate the final price.

The Total Price section will update with applied discounts.


Technologies Used

Python 3.11+

Django 4.x

Bootstrap 5

HTML, CSS,js

Project Structure

coficheckout/
│
├── store/
│   ├── templates/store/        # HTML templates for the store (checkout pages)
│   │   ├── checkout.html
│   │
│   │
│   ├── forms.py               # Django forms (cart forms, discount forms)
│   │   └── CartForm, DiscountForm
│   │
│   ├── models.py              # Django models (Code, Name, Price)
│   │   └── Code, Name, Price
│   │
│   ├── admin.py               # Register models for Django admin panel
│   │
│   ├── views.py               # Logic for checkout, cart, discounts
│   │
│   ├── urls.py                # Routes for the store app 
│   │
│
├── checkout.py                # Optional project-level helper (like payment integration)
├── config.json             
├── manage.py                  # Django CLI
└── README.md                  # Project documentation

Unit Test Section

##  Running Unit Tests

This project includes a full set of **unit tests** to ensure all discount rules and checkout logic work correctly.

### **Test Coverage**
The tests cover:
- Empty cart total should be 0  
- 2-for-1 promotion for `VOUCHER` items  
- Bulk discount for `TSHIRT` (3 or more → 19.00€ each)  
- SWAG pack discount (TSHIRT + VOUCHER + MUG = 25.00€)  
- Mixed scenarios with multiple discounts applied  

### **Folder Structure**
The test files are located under the `store/test/` directory:


### **How to Run the Tests**

**Navigate to the project root folder** (where `manage.py` is located):
```bash
cd coficheckout

**Run the test suite:**

python manage.py test store

**Verbose mode (see detailed test names and results):**

python manage.py test store -v 2

## Test Coverage


1. **Run Tests with Coverage**
   ```bash
   coverage run manage.py test
   coverage report -m


---

### **Why Add This**
- Helps contributors understand how well your project is tested.  
- Makes it easier to maintain **high test coverage**.  
- Provides **step-by-step instructions** for new developers.





