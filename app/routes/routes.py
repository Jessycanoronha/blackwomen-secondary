from flask import Blueprint, jsonify, request
from app.models.models import db, Woman, create_table_if_not_exists
import requests
from requests.exceptions import RequestException

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/women', methods=['GET'])
def get_women():
    try:
        women = Woman.query.all()

        women_json = []
        for woman in women:
            women_json.append({
                'id': woman.id,
                'name': woman.title,
                'description': woman.description,
                'image_url': woman.image_url,
                'slug': woman.slug,
                'order': woman.order,
                'credits': woman.credits,
                'country': woman.country,
                'birthdate': woman.birthdate,
                'deathdate': woman.deathdate
            })

        return jsonify(women_json), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/women/<int:order>', methods=['GET'])
def get_figure(order):
    figure = Woman.query.filter_by(order=order).first_or_404()
    return jsonify(figure.serialize()), 200

@bp.route('/woman', methods=['POST'])
def create_figure():
    data = request.get_json()
    new_woman = Woman(id=data['id'],order=data['order'], slug=data['slug'], title=data['title'], description=data['description'], image_url=data['image_url'], credits=data['credits'], country=data['country'], birthdate=data['birthdate'], deathdate=data['deathdate'])
    db.session.add(new_woman)
    db.session.commit()
    return jsonify(new_woman.serialize()), 201

@bp.route('/women/<int:id>', methods=['PUT'])
def update_woman(id):
    woman = Woman.query.get_or_404(id)
    data = request.get_json()
    
    woman.title = data.get('title', woman.title)
    woman.description = data.get('description', woman.description)
    woman.image_url = data.get('image_url', woman.image_url)
    woman.additional_metadata = data.get('additional_metadata', woman.additional_metadata)
    woman.order = data.get('order', woman.order)
    woman.slug = data.get('slug', woman.slug)
    woman.country = data.get('country', woman.country)
    woman.birthdate = data.get('birthdate', woman.birthdate)
    woman.deathdate = data.get('deathdate', woman.deathdate)
    woman.credits = data.get('credits', woman.credits)
    
    db.session.commit()
    return jsonify(woman.to_dict()), 200

@bp.route('/women/<string:id>', methods=['DELETE'])
def delete_figure(id):
    figure = Woman.query.get_or_404(id)
    db.session.delete(figure)
    db.session.commit()
    return jsonify({'message': 'Woman deleted successfully'}), 200

@bp.route('/women/<string:id>', methods=['PATCH'])
def partially_update_woman(id):
    woman = Woman.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        woman.title = data['title']
    if 'description' in data:
        woman.description = data['description']
    if 'image_url' in data:
        woman.image_url = data['image_url']
    if 'additional_metadata' in data:
        woman.additional_metadata = data['additional_metadata']
    if 'order' in data:
        woman.order = data['order']
    if 'slug' in data:
        woman.slug = data['slug']
    if 'country' in data:
        woman.country = data['country']
    if 'birthdate' in data:
        woman.birthdate = data['birthdate']
    if 'deathdate' in data:
        woman.deathdate = data['deathdate']
    if 'credits' in data:
        woman.credits = data['credits']
    
    db.session.commit()
    return jsonify(woman.serialize()), 200



