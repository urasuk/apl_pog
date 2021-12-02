# rest
BASE_PATH = '/api/v15/'
USER_PATH = '/user'
MEDICINE_PATH = '/medicine'
PHARMACY_PATH = '/pharmacy'
PHARMACY_ORDERS_PATH = '/pharmacy/orders'
PHARMACY_ORDERS_MEDICINES_PATH = '/pharmacy/orders/medicines'
PHARMACY_PATH3 = '/pharmacy3'
DEMAND_MEDICINE_PATH = '/demand/medicine'

MEDICINE_CATEGORY = '/medicine/category'

# general messages
SOMETHING_WENT_WRONG = 'Ooooops....Something went wrong'
CANT_CHANGE_ID = 'Sorry, but ID cannot be changed'

# user messages
USER_ALREADY_EXISTS = 'User already exists, provide unique id'
USER_CREATED = 'User successfully created'
USER_NOT_FOUND = 'User not found'
USER_UPDATED = 'User successfully updated'
USER_DELETED = 'User successfully deleted'

# medicine messages
MEDICINE_PLACED = 'Medicine successfully placed'
MEDICINE_NOT_FOUND = 'Medicine not found'
MEDICINE_EDITED = 'Medicine successfully edited'
MEDICINE_DELETED = 'Medicine successfully deleted'
MEDICINE_ADDED_TO_ORDER = 'Medicine successfully added to order'
MEDICINE_DELETED_FROM_ORDER = 'Medicine successfully deleted from order'
MEDICINE_ALREADY_EXIST = 'Medicine already exists, provide unique id'
INCORRECT_STATUS = 'The status of a medicine is incorrect!'
DEMAND_EDITED = 'Your demand has been successfully edited!'

# order messages
order_statuses = ['placed', 'approved', 'delivered']
ORDER_CREATED = 'Order successfully created'
ORDER_UPDATED = 'Order successfully updated'
ORDER_DELETED = 'Order successfully deleted'
ORDER_NOT_FOUND = 'Order not found'
ORDER_ALREADY_EXIST = 'Order already exists, provide unique id'

# authentification
INCORRECT_USERNAME = "There`s no such username! Please,enter a right one"
BAD_PASSWORD = "Bad password! Please,enter a right one"
ACCESS_DENIED = "Access denied! The operation is forbidden for you"

#access levels
ADMIN = 'admin'
USER = 'user'

