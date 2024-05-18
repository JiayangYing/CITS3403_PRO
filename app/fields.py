from flask import current_app
from wtforms import SelectField, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget
from flask_wtf.file import MultipleFileField, FileAllowed

# Conditions options
conditions = [
    ('', '--Select Condition--'), 
    ('Brand New', 'Brand New'), 
    ('Used - Good', 'Used - Good'),
    ('Used - Fair', 'Used - Fair'), 
    ('Other', 'Other')
]

# Categories options
categories = [
    ('', '--Select Category--'), 
    ('Clothing & Accessories', 'Clothing & Accessories'), 
    ('Home & Garden', 'Home & Garden'), 
    ('Electronics', 'Electronics'), 
    ('Books & Media', 'Books & Media'), 
    ('Sport & Leisure', 'Sport & Leisure'),
    ('Others', 'Others')
]

# Price ranges options
ranging = 100
prices = \
    [('', 'Any')] +\
    [(f'{x}-{x+ranging-1}', f'{x}-{x+ranging-1}') for x in range(1, 1000, ranging)] +\
    [('1000', '> 1000')]

price_range_map = {}
for price_range_str, _ in prices:
    if price_range_str:  # Skip empty string
        if '-' in price_range_str:  # If the price range contains a hyphen
            start, end = map(int, price_range_str.split('-'))
            price_range_map[price_range_str] = (start, end)
        else:  # For "more than 100"
            start = int(price_range_str)
            price_range_map[price_range_str] = (start, None)

class ProductConditionField(SelectField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the choices for the field
        self.choices = conditions

class ProductConditionMultipleCheckboxField(SelectMultipleField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = ListWidget(prefix_label=False)
        self.option_widget = CheckboxInput()
        self.choices = conditions[1:]
        
class ProductCategoryField(SelectField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = categories

class ProductCategoryMultipleCheckboxField(SelectMultipleField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = ListWidget(prefix_label=False)
        self.option_widget = CheckboxInput()
        self.choices = categories[1:]

class ProductPriceRangeField(SelectField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = prices
        
class ProductImagesField(MultipleFileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exts = current_app.config['UPLOAD_EXTENSIONS']
        self.validators=[
            FileAllowed(
                [ext.replace('.','') for ext in exts], 
                message = f'Invalid File Type. Must be {", ".join(exts)}' 
            )]