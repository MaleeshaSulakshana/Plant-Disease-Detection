import dbConnector as dbConn


# Function for get plant names
def select_plants():
    conn = dbConn.db_connector()

    select_plants = ''' SELECT DISTINCT(plant_name) FROM diseases '''
    cur = conn.cursor()
    cur.execute(select_plants)
    return cur.fetchall()


# Function for get plant diseases
def select_diseases():
    conn = dbConn.db_connector()

    select_diseases = ''' SELECT id, plant_name, disease_name, thumbnail FROM diseases '''
    cur = conn.cursor()
    cur.execute(select_diseases)
    return cur.fetchall()


# Function for get disease details
def get_disease_details(id):
    conn = dbConn.db_connector()

    select = ''' SELECT plant_name, disease_name, disease_details,
                        treatment_details, thumbnail, image1, image2, image3, image4 FROM diseases WHERE id = %s '''
    value = (str(id),)

    cur = conn.cursor()
    cur.execute(select, value)
    return cur.fetchall()


# Function for add new disease
def prediction_count(date, accuracy):
    try:
        conn = dbConn.db_connector()

        query = """ INSERT INTO prediction_count (date, count, accuracy) SELECT * FROM (SELECT %s, 1, %s) AS tmp
                    WHERE NOT EXISTS ( SELECT date FROM prediction_count WHERE date = %s ) """
        values = (str(date), float(accuracy), str(date))
        cur = conn.cursor()
        cur.execute(query, values)

        if cur.rowcount < 1:
            query = """ UPDATE prediction_count SET count = count + 1, accuracy = (accuracy + %s) WHERE date= %s """
            value = (float(accuracy), str(date))
            cur = conn.cursor()
            cur.execute(query, value)

        conn.commit()
        return True

    except Exception as e:
        return False


# Function for get plant diseases
def search_diseases(search):
    conn = dbConn.db_connector()

    select = ''' SELECT id, plant_name, disease_name, thumbnail FROM diseases 
                                WHERE disease_name LIKE %s OR plant_name LIKE %s '''
    values = (('%' + str(search) + '%'), ('%' + str(search) + '%'))
    cur = conn.cursor()
    cur.execute(select, values)
    return cur.fetchall()
