import dbConnector as dbConn


# Function for admin login
def admin_login(email, psw):
    conn = dbConn.db_connector()

    query = ''' SELECT id FROM admin WHERE email = %s AND psw = %s '''
    values = (str(email), str(psw))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for check disease is exists
def check_disease_is_exist(txt_plant_name, txt_disease_name):
    conn = dbConn.db_connector()

    select = ''' SELECT COUNT(*) FROM diseases WHERE plant_name = %s AND disease_name = %s '''
    values = (str(txt_plant_name), str(txt_disease_name))
    cur = conn.cursor()
    cur.execute(select, values)

    return cur.fetchall()[0][0]


# Function for add new disease
def add_new_disease(disease_id, txt_plant_name, txt_disease_name, txt_disease_detail, txt_treatment_detail,
                    thumbnail, image1, image2, image3, image4):
    conn = dbConn.db_connector()

    insert_data = ''' INSERT INTO diseases (id, plant_name, disease_name, disease_details,
                        treatment_details, thumbnail, image1, image2, image3, image4) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
    values = (str(disease_id), str(txt_plant_name), str(txt_disease_name), str(txt_disease_detail),
              str(txt_treatment_detail), str(thumbnail), str(image1), str(image2), str(image3), str(image4))
    cur = conn.cursor()
    cur.execute(insert_data, values)

    conn.commit()
    return cur.rowcount


# Function for get diseases details for view
def get_diseases_details():
    conn = dbConn.db_connector()

    select = ''' SELECT id, plant_name, disease_name, thumbnail, image1, image2, image3, image4 FROM diseases '''

    cur = conn.cursor()
    cur.execute(select)
    return cur.fetchall()


# Function for get diseases details for update
def disease_details(id):
    conn = dbConn.db_connector()

    select = ''' SELECT id, plant_name, disease_name, disease_details, treatment_details,
                         thumbnail, image1, image2, image3, image4 FROM diseases WHERE id = %s'''

    cur = conn.cursor()
    cur.execute(select, (str(id),))
    return cur.fetchall()


# Function for update disease details
def update_disease_details(txt_id, txt_plant_name, txt_disease_name, txt_disease_detail, txt_treatment_detail):
    conn = dbConn.db_connector()

    update = ''' UPDATE diseases SET plant_name = %s, disease_name = %s, disease_details = %s,
                        treatment_details = %s WHERE id = %s '''
    values = (str(txt_plant_name), str(txt_disease_name), str(txt_disease_detail),
              str(txt_treatment_detail), str(txt_id))
    cur = conn.cursor()
    cur.execute(update, values)

    conn.commit()
    return cur.rowcount


# Function for delete disease details
def delete_disease_details(id):
    conn = dbConn.db_connector()

    delete = ''' DELETE FROM diseases WHERE id = %s '''
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(delete, value)

    conn.commit()
    return cur.rowcount


# For admin
# Function for get all admins recodes
def get_all_admin_recodes(id):
    conn = dbConn.db_connector()

    select = ''' SELECT id, name, email FROM admin WHERE id != %s'''

    cur = conn.cursor()
    cur.execute(select, (str(id),))
    return cur.fetchall()


# Function for add new admin recode
def add_new_admin_recode(id, name, email, psw):
    conn = dbConn.db_connector()

    insert = ''' INSERT INTO admin (id, name, email, psw) VALUES (%s, %s, %s, %s) '''
    values = (str(id), str(name), str(email), str(psw))
    cur = conn.cursor()
    cur.execute(insert, values)

    conn.commit()
    return cur.rowcount


# Function for update admin recode details
def update_admin_recode_details(id, name):
    conn = dbConn.db_connector()

    update = ''' UPDATE admin SET name = %s WHERE id = %s '''
    values = (str(name), str(id))
    cur = conn.cursor()
    cur.execute(update, values)

    conn.commit()
    return cur.rowcount


# Function for delete admin recode
def delete_admin_recode(id):
    conn = dbConn.db_connector()

    delete = ''' DELETE FROM admin WHERE id = %s '''
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(delete, value)

    conn.commit()
    return cur.rowcount


# Function for check email exist
def email_exist(email):
    conn = dbConn.db_connector()

    select = ''' SELECT COUNT(*) FROM admin WHERE email = %s'''
    value = (str(email),)
    cur = conn.cursor()
    cur.execute(select, value)

    return cur.fetchall()[0][0]


# Function for get logged admin details
def get_admin_details(id):
    conn = dbConn.db_connector()

    select = ''' SELECT id, name, email FROM admin WHERE id = %s'''

    cur = conn.cursor()
    cur.execute(select, (str(id),))
    return cur.fetchall()


# Function for update admin psw
def update_admin_psw(id, psw):
    conn = dbConn.db_connector()

    update = ''' UPDATE admin SET psw = %s WHERE id = %s '''
    values = (str(psw), str(id))
    cur = conn.cursor()
    cur.execute(update, values)

    conn.commit()
    return cur.rowcount


# Function for update admin recovery psw
def update_admin_recovery_psw(email, psw):
    conn = dbConn.db_connector()

    update = ''' UPDATE admin SET psw = %s WHERE email = %s '''
    values = (str(psw), str(email))
    cur = conn.cursor()
    cur.execute(update, values)

    conn.commit()
    return cur.rowcount


# Function for get prediction count
def get_week_prediction_count():
    conn = dbConn.db_connector()

    select = ''' SELECT date, count FROM prediction_count ORDER BY date DESC LIMIT 7 '''
    cur = conn.cursor()
    cur.execute(select)
    return cur.fetchall()


# Function for get prediction count
def get_prediction_count():
    conn = dbConn.db_connector()

    select = ''' SELECT SUM(count) FROM prediction_count '''
    cur = conn.cursor()
    cur.execute(select)
    return cur.fetchall()[0][0]


# Function for get prediction count
def get_prediction_accuracy():
    conn = dbConn.db_connector()

    select = ''' SELECT date, (accuracy/count) FROM prediction_count ORDER BY date DESC LIMIT 7 '''
    cur = conn.cursor()
    cur.execute(select)
    return cur.fetchall()


# Function for get plant & diseases
def get_plant_diseases_count():
    conn = dbConn.db_connector()

    select = ''' SELECT plant_name, COUNT(plant_name) FROM diseases GROUP BY plant_name '''
    cur = conn.cursor()
    cur.execute(select)
    return cur.fetchall()


# Function for get admin name
def get_admin_name(id):
    data = []
    conn = dbConn.db_connector()

    select = ''' SELECT name FROM admin WHERE id = %s '''
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(select, value)
    return cur.fetchall()


# Function for get disease count for check exist
def is_exist_disease(id):
    conn = dbConn.db_connector()

    select = ''' SELECT COUNT(*) FROM diseases WHERE id = %s '''
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(select, value)
    return cur.fetchall()[0][0]


# Function for get image details
def get_disease_image_name(column, id):
    conn = dbConn.db_connector()

    select = ''' SELECT {} FROM diseases WHERE id = %s '''.format(str(column))
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(select, value)
    return cur.fetchall()[0][0]


# Function for update admin psw
def update_disease_image(column, image, id):
    conn = dbConn.db_connector()

    update = ''' UPDATE diseases SET {} = %s 
                            WHERE id = %s '''.format(str(column))
    values = (str(image), str(id))
    cur = conn.cursor()
    cur.execute(update, values)

    conn.commit()
    return cur.rowcount
