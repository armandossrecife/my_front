from entidades import User, File

class UserDAO:
    def __init__(self, db):
        self.db = db

    def create_user(self, user):
        if self.user_by_email(user.email) or self.user_by_username(user.username):
            raise ValueError('User with this email or username already exists')
        self.db.session.add(user)
        self.db.session.commit()

    def user_by_id(self, user_id):
        return User.query.get(user_id)

    def user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def update_user(self, user_id, name, username, email, password, profile_picture_url=None):
        user = User.query.get(user_id)
        if user:
            if name is not None:
                user.name = name
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if password is not None:
                user.password = password  # In production, hash the password.
            if profile_picture_url is not None:
                user.profile_picture_url = profile_picture_url  # Update profile picture URL

            try:
                self.db.session.commit()
                return user
            except Exception as e:
                self.db.session.rollback()  # Important to rollback in case of error.
                print(f"Error updating user: {e}")  # Log the error.
                return None
        else:
            return None
        
    def update_password(self, user_id, new_password):
        """
        Update the password for a user with the given user_id.    
        Args:
            user_id (int): The ID of the user whose password will be updated.
            new_password (str): The new password to set for the user.        
        Returns:
            User: The updated user object if successful, None otherwise.
        """
        user = self.user_by_id(user_id)
        if user:
            # Hash the new password before saving it to the database
            # hashed_password = generate_password_hash(new_password, method='sha256')
            user.password = new_password # hashed_password
            try:
                self.db.session.commit()
                return user
            except Exception as e:
                self.db.session.rollback()  # Rollback in case of error
                print(f"Error updating password: {e}")  # Log the error
                return None
        else:
            return None

    def delete_user_by_id(self, user_id):
        user = self.user_by_id(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()

    def list_users(self):
        return User.query.all()

    def link_to_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise ValueError('User not found')
            file = File.query.filter_by(id=file.id).first()
            if not file:
                raise ValueError('File not found')
            user.my_files.append(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during file to user - {ve}')

    def link_to_files(self, user_id, files):
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise ValueError('User not found')
            for each in files:
                file = File.query.filter_by(id=each.id).first()
                user.my_files.append(file)    
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during files to user - {ve}')

    def unlink_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise ValueError('User not found')
            file = File.query.filter_by(id=file.id).first()
            if not file:
                raise ValueError('File not found')
            user.my_files.remove(file)
            self.db.session.commit()
        except Exception as e:
            raise Exception(f'Error during remove file from user - {e}')

    def list_all_files(self, user_id):
        user = User.query.filter_by(id=user_id).first()        
        return user.my_files

    def get_file_by_user(self, name):        
        return User.my_files.query.get(name)

    def get_file_by_user_by_id(self, id):        
        return User.my_files.query.get(id)

class FilesDAO:
    def __init__(self, db):
        self.db = db

    def insert_file(self, file):
        try:
            self.db.session.add(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during insert file - {ve}')

    def query_file_by_name(self, p_name):
        file = File.query.filter_by(name=p_name).first()
        return file

    def query_file_by_id(self, p_id):
        file = File.query.filter_by(id=p_id).first()
        return file
    
    def list_all_files(self):
        return File.query.all()

    def delete_file(self, file):
        try:
            file = File.query.filter_by(id=file.id).first()
            if not file:
                raise ValueError('File not found')
            self.db.session.delete(file)
            self.db.session.commit()
        except ValueError as ve:
            raise ValueError(f'Error during delete file - {ve}')