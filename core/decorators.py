from django.shortcuts import redirect


def is_user(func):
    
    def check_user(req):
        try:
            
            if req.session["logged_in"]:
                print(req.session["logged_in"],"logged_in")

                return func(req)
            else:
                return redirect('signin')

        except:
            return redirect('signin')
    return check_user