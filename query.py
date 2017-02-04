"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

    #BaseQuery

# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

    #When there is a many-to-many relationship between two tables,
    #an association table is used (generally named "FirsttableSecondtable")
    #to connect the two tables. It contains primary keys of the respective tables.
    #The two tables each has a one to many relationship with the
    #association table.


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the ``id`` of "ram."
q1 = Brand.query.filter_by(brand_id='ram').one()

# Get all models with the name "Corvette" and the brand_id "che."
q2 = Model.query.filter((Model.name == 'Corvette') & (Model.brand_id == 'che')).all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor."
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter((Brand.founded == 1903) & (Brand.discontinued.is_(None))).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter((Brand.discontinued.isnot(None) | (Brand.founded < 1950))).all()

# Get any model whose brand_id is not "for."
q8 = Model.query.filter(Model.brand_id != 'for').first()


# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query.

        >>> get_model_info(1960)
        model=Corvette brand=Chevrolet HQ=Detroit, Michigan
        model=Corvair brand=Chevrolet HQ=Detroit, Michigan
        model=Rockette brand=Fairthorpe HQ=Chalfont St Peter, Buckinghamshire

    """

    models = Model.query.options(db.joinedload('brand')).filter_by(year=year).all()

    for model in models:
        print "model=%s brand=%s HQ=%s" % (model.name, model.brand.name, model.brand.headquarters)


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query."""

    brands = db.session.query(Brand, Model).outerjoin(Model).all()

    for brand, model in brands:
        if model is None:
            print "Brand: %s has no models" % (brand.name)
        else:
            print "Brand: %s, model: %s (%d)" % (brand.name, model.name, model.year)


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string.

        >>> search_brands_by_name('le')
        [<brand_id=chr name=Chrysler HQ=Auburn Hills, Michigan founded=1925>, <brand_id=che name=Chevrolet HQ=Detroit, Michigan founded=1911>, <brand_id=ram name=Rambler HQ=Kenosha, Washington founded=1901>]

    """

    keyword = "%" + "%s" % (mystr) + "%"

    brands = Brand.query.filter(Brand.name.like(keyword)).all()

    return brands


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive).

        >>> get_models_between(1950, 1954)
        [<model_id=4 name=Minx Magnificent year=1950 brand_id=hil>, <model_id=5 name=Corvette year=1953 brand_id=che>]
    """

    models = Model.query.filter((Model.year >= start_year) & (Model.year < end_year)).all()

    return models


if __name__ == "__main__":
    print
    import doctest
    if doctest.testmod().failed == 0:
        print "*** ALL TESTS PASSED ***"
    print
