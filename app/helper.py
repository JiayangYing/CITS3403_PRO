from sqlalchemy import select
from app.models import Product,Image
from app.fields import price_range_map
from flask import url_for, current_app
from app.blueprint import main
import os

class FilterHelper:
    @staticmethod
    def generate_query(search_form):
        query = select(Product).where(Product.is_active)  # Initialize an empty query
        if search_form.categories.data:
            query = query.where(Product.category.in_(search_form.categories.data))
        if search_form.conditions.data:
            query = query.where(Product.condition.in_(search_form.conditions.data))
        price_start, price_end = price_range_map.get(search_form.price.data, (None, None))
        if price_start is not None:
            if price_end is None:  # Handle "more than 100"
                query = query.where(Product.price >= price_start)
            else:
                query = query.where(Product.price.between(price_start, price_end))
        return query
 
    @staticmethod
    def filters_as_dict(search_form):
        filters_dict = {}
        for field_name in search_form:
            if field_name not in ['csrf_token', 'submit']:
                if field_name == 'price':
                    filters_dict[field_name] = search_form.get(field_name)
                else:
                    filters_dict[field_name] = search_form.getlist(field_name)
        return filters_dict
    
 
class PaginatorHelper:
    def __init__(self, endpoint, page, has_prev, has_next, prev_num, next_num, **view_args):
        self.endpoint = endpoint
        self.page = page
        self.has_prev = has_prev
        self.has_next = has_next
        self.prev_num = prev_num
        self.next_num = next_num
        self.view_args = view_args
 
    def get_pagination(self):
        next_url, prev_url, pages = None, None, []
        if self.has_prev:
            prev_url = url_for(self.endpoint, page=self.prev_num, **self.view_args)
            pages.append(self.page - 1)
        pages.append(self.page)
        if self.has_next:
            next_url = url_for(self.endpoint, page=self.next_num, **self.view_args)
            pages.append(self.page + 1)
        return next_url, prev_url, pages
    

class ProductHelper:
    @staticmethod
    def get_images_path(product_id):
        img_dir = os.path.join('static', 'img', 'product_image', str(product_id))
        full_dir = os.path.join(main.root_path, img_dir)
        extensions = tuple(current_app.config['UPLOAD_EXTENSIONS'])
        path_images = []
        for img in os.listdir(full_dir):
            if img.lower().endswith(extensions):
                path_images.append(f'/{img_dir}/{img}')
        return path_images

    @staticmethod
    def get_main_image_path(product_id, img_id):
        img_dir = os.path.join('static', 'img', 'product_image', str(product_id))
        full_dir = os.path.join(main.root_path, img_dir)
        extensions = current_app.config['UPLOAD_EXTENSIONS']
        for ext in extensions:
            img_filename = f"{img_id}{ext}"
            img_path = os.path.join(full_dir, img_filename)
            if os.path.exists(img_path):
                return f'/{os.path.join(img_dir, img_filename)}'
        return None
