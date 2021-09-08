import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("file_name")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://social-acceptance-fc45b-default-rtdb.firebaseio.com/'
})

ref = db.reference("/")
ref.set({
	"Books":
	{
		"Best_Sellers": -1
	}
})