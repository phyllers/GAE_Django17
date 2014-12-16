function check_user(is_authenticated){
    console.log('in check user and user authenticated is ' + is_authenticated);
    if (!is_authenticated){
        console.log('signing out');
        google.identitytoolkit.signOut();
    }
}