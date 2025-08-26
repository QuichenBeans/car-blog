from app import db, app, Cars


@app.route('/add_car', methods='POST')
def add_car():
    hatchback = [
        {"brand": "Skoda", "model": 'Fabia', 'colour': 'Blue', 'doors': 5, 'safety_rating': '4/5'},
        {'brand': 'VW', 'model': 'Golf', 'colour': 'grey', 'doors': 5, 'safety_rating': '5/5'},
        {'brand': 'Audi', 'model': 'A1', 'colour': 'black', 'doors': 5, 'safety_rating': '4/5'}
]
    suv = [
        {'brand': 'Range Rover', 'model': 'Defender', 'colour': 'green', 'doors': 5, 'safety_rating': '4/5'},
        {'brand': 'Toyota', 'model': 'Hilux', 'colour': 'red', 'doors': 5, 'safety_rating': '5/5'},
        {'brand': 'Jeep', 'model': 'Wrangler', 'colour': 'blue', 'doors': 5, 'safety_rating': '4/5'}
]
    supercar = [
        {'brand': 'Ferrari', 'model': 'F40', 'colour': 'red','doors': 3, 'safety_rating': '2/5'},
        {'brand': 'Aston Martin', 'model': 'DD10', 'colour': 'green', 'doors': 3, 'safety_rating': '4/5'},
        {'brand': 'McLaren', 'model': 'P1', 'colour': 'red', 'doors': 3, 'safety_rating': '3/5'}
]
    electric = [
        {'brand': 'Tesla', 'model': 'Model X', 'colour': 'white', 'doors': 5, 'safety_rating': '5/5'},
        {'brand': 'BMW', 'model': 'i3', 'colour': 'blue and black', 'doors': 5, 'safety_rating': '5/5'},
        {'brand': 'Renault', 'model': '5', 'colour': 'yellow', 'doors': 5, 'safety_rating': '4.5/5'}
]

    hatch = Cars.query.filter_by(car_type='hatchback').first()
    if not hatch:
        hatch = Cars(car_type='hatchback', content=hatchback)
        db.session.add(hatch)
    else:
        hatch.content = hatchback
    db.session.commit()
    
    sports_vec = Cars.query.filter_by(car_type='suv').first()
    if not sports_vec:
        sports_vec = Cars(car_type='suv', content=suv)
        db.session.add(sports_vec)
    else:
        sports_vec.content = suv
    db.session.commit()
    
    supe = Cars.query.filter_by(car_type='supercar').first()
    if not supe:
        supe = Cars(car_type='supercar', content=supercar)
        db.session.add(supe)
    else:
        supe.content = supercar
    db.session.commit()
    
    ev = Cars.query.filter_by(car_type='electric').first()
    if not ev:
        ev = Cars(car_type='electric', content=electric)
        db.session.add(ev)
    else:
        ev.content = electric

    db.session.commit()