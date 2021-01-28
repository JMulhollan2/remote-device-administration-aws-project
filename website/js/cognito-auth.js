////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// This code was taken from an AWS workshop, and for the majority is not my code. 
///
/// This code however has been adapted, and extra functions have been marked out below.
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

var Telemetry = window.Telemetry || {};

(function scopeWrapper($) {
    var signinUrl = '/signin.html';

    var poolData = {
        UserPoolId: _config.cognito.userPoolId,
        ClientId: _config.cognito.userPoolClientId
    };

    var userPool;

    if (!(_config.cognito.userPoolId &&
          _config.cognito.userPoolClientId &&
          _config.cognito.region)) {
        $('#noCognitoMessage').show();
        return;
    }

    userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    if (typeof AWSCognito !== 'undefined') {
        AWSCognito.config.region = _config.cognito.region;
    }

    Telemetry.signOut = function signOut() {
        userPool.getCurrentUser().signOut();
    };

    Telemetry.changePassword = function changePassword(event){
        handleChangePassword(event);
    };

    // Reset password functionality - added by me.
    Telemetry.resetPassword = function resetPassword(event){
        result = handleResetPassword(event);
        return result
    };

    Telemetry.confirmResetPassword = function confirmResetPassword(email, event){
        handleConfirmResetPassword(event, email)
    };
    // End reset password functions

    Telemetry.authToken = new Promise(function fetchCurrentAuthToken(resolve, reject) {
        var cognitoUser = userPool.getCurrentUser();

        if (cognitoUser) {
            cognitoUser.getSession(function sessionCallback(err, session) {
                if (err) {
                    reject(err);
                } else if (!session.isValid()) {
                    resolve(null);
                } else {
                    resolve(session.getIdToken().getJwtToken());
                }
            });
        } else {
            resolve(null);
        }
    });


/*
* Cognito User Pool functions
*/

    function register(email, password, onSuccess, onFailure) {
        var dataEmail = {
            Name: 'email',
            Value: email
        };
        var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

        userPool.signUp(email, password, [attributeEmail], null,
            function signUpCallback(err, result) {
                if (!err) {
                    onSuccess(result);
                } else {
                    onFailure(err);
                }
            }
        );
    }

    function signin(email, password, onSuccess, onFailure) {
        var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails({
            Username: email,
            Password: password
        });

        var cognitoUser = createCognitoUser(email);
        cognitoUser.authenticateUser(authenticationDetails, {
            onSuccess: onSuccess,
            onFailure: onFailure
        });
    }

    function verify(email, code, onSuccess, onFailure) {
        createCognitoUser(email).confirmRegistration(code, true, function confirmCallback(err, result) {
            if (!err) {
                onSuccess(result);
            } else {
                onFailure(err);
            }
        });
    }

    function createCognitoUser(email) {
        return new AmazonCognitoIdentity.CognitoUser({
            Username: email,
            Pool: userPool
        });
    }

    /*
     *  Event Handlers
     */

    $(function onDocReady() {
        $('#signinForm').submit(handleSignin);
        $('#registrationForm').submit(handleRegister);
        $('#verifyForm').submit(handleVerify);
        handleSessionForNavBar();
    });

    // Nav bar logic by me - easiest place to put is here.
    function updateNavBar(email) {
        var body = document.getElementById("signInBtn");
        body.outerHTML = ""
        var body = document.getElementById("registerBtn");
        body.outerHTML = ""

        var nav_bar = document.getElementById("top-nav-bar");
        var sign_out_li = document.createElement("li");
        sign_out_li.id = "signOutLi";
        sign_out_li.style = "float:right";
        var sign_out_a = document.createElement("a");
        sign_out_a.className = "nav-bar-content";
        sign_out_a.id = "signOut"
        var sign_out_text = document.createTextNode("Sign out");
        sign_out_a.appendChild(sign_out_text);
        sign_out_li.appendChild(sign_out_a);
        nav_bar.appendChild(sign_out_li);

        var nav_bar = document.getElementById("top-nav-bar");
        var devices_li = document.createElement("li");
        devices_li.id = "devicesLi";
        devices_li.style = "float:right";
        var devices_a = document.createElement("a");
        devices_a.className = "nav-bar-content";
        devices_a.id = "userEmail"
        devices_a.href = "devices.html" 
        var devices_text = document.createTextNode("Devices");
        devices_a.appendChild(devices_text);
        devices_li.appendChild(devices_a);
        nav_bar.appendChild(devices_li);

        var nav_bar = document.getElementById("top-nav-bar");
        var user_email_li = document.createElement("li");
        user_email_li.id = "userEmailLi";
        user_email_li.style = "float:right";
        var user_email_a = document.createElement("a");
        user_email_a.className = "nav-bar-content";
        user_email_a.id = "userEmail"
        var user_email_text = document.createTextNode(email);
        user_email_a.appendChild(user_email_text);
        user_email_li.appendChild(user_email_a);
        nav_bar.appendChild(user_email_li);

        $('#signOut').click(function() {
            Telemetry.signOut();
            alert("You have been signed out.");
            window.location = "signin.html";
        });
    }

    // This function will help control the session if a user is logged in, and modify the navbar to show this.
    function handleSessionForNavBar() {
        var cognitoUser = userPool.getCurrentUser();
        if (cognitoUser != null) {
            cognitoUser.getSession(function(err, session) {
                if (err) {
                    alert(err);
                    return;
                }
                console.log('session validity: ' + session.isValid());
            });
            var path = window.location.pathname;
            var page = path.split("/").pop();
            if (page == "devices.html"){}
            else if (page == "signin.html" || page == "verify.html" || page == "register.html" || page == "forgotpassword.html"){
                window.location.href = 'devices.html'; // This needs to be changed in the future when the website structure is updated.
            }
            else {
                var email = cognitoUser.getUsername()
                updateNavBar(email);
            }
        }
    }

    function handleSignin(event) {
        var email = $('#emailInputSignin').val();
        var password = $('#passwordInputSignin').val();
        event.preventDefault();
        signin(email, password,
            function signinSuccess() {
                console.log('Successfully Logged In');
                window.location.href = 'devices.html';
            },
            function signinError(err) {
                alert(err);
            }
        );
    }

    function handleChangePassword(event) {
        var old_password = $('#oldPasswordInputChangePassword').val();
        var new_password_1 = $('#newPasswordInput1ChangePassword').val();
        var new_password_2 = $('#newPasswordInput2ChangePassword').val();
        var cognitoUser = userPool.getCurrentUser();

        if (cognitoUser != null) {
            cognitoUser.getSession(function(err, session) {
                if (err) {
                    alert(err);
                }
                console.log('session validity: ' + session.isValid());
            });
        }

        if (new_password_1 == new_password_2) {
            cognitoUser.changePassword(old_password, new_password_1, function(err, result) {
                if (!err) {
                    alert(result);
                } else {
                    alert(err);
                }
            });
        }
        else {
            alert('Passwords do not match!');
        }
    }

    // Reset password functionality - added by me.
    function handleResetPassword(event) {
        var email = $('#emailInputSignin').val();
        cognitoUser = new AmazonCognitoIdentity.CognitoUser({
            Username: email,
            Pool: userPool
        });
        cognitoUser.forgotPassword({
            onSuccess: function (result) {
                // This should do something - this function is bugged on AWS's side.
            },
            onFailure: function(err) {
                // Intentionally left blank.
            }
        });
        return true
    }

    function handleConfirmResetPassword(event, email) {
        var verificationCode = $('#verificationCodeInput').val();
        var newPasswordInput1 = $('#password1Input').val();
        var newPasswordInput2 = $('#password2Input').val();

        cognitoUser = new AmazonCognitoIdentity.CognitoUser({
            Username: email,
            Pool: userPool
        });

        if (newPasswordInput1 == newPasswordInput2){
            cognitoUser.confirmPassword(verificationCode, newPasswordInput1, {
                onFailure(err) {
                    alert(err);
                },
                onSuccess() {
                    alert("Password change successful, you will now be directed to the login page.")
                    window.location.href = 'signin.html';
                },
            });
        }
        else {
            alert('Passwords do not match!');
        }
    }
    // End of reset password functions

    function handleRegister(event) {
        var email = $('#emailInputRegister').val();
        var password = $('#passwordInputRegister').val();
        var password2 = $('#password2InputRegister').val();

        var onSuccess = function registerSuccess(result) {
            var cognitoUser = result.user;
            console.log('user name is ' + cognitoUser.getUsername());
            var confirmation = ('Registration successful. Please check your email inbox or spam folder for your verification code.');
            if (confirmation) {
                window.location.href = 'verify.html';
            }
        };
        var onFailure = function registerFailure(err) {
            if (err.toString().includes("Invalid JSON")){
                alert ("Email is already in use!")
            }
            else{
                alert(err);
            }
        };
        event.preventDefault();

        if (password === password2) {
            register(email, password, onSuccess, onFailure);
        } else {
            alert('Passwords do not match');
        }
    }

    function handleVerify(event) {
        var email = $('#emailInputVerify').val();
        var code = $('#codeInputVerify').val();
        event.preventDefault();
        verify(email, code,
            function verifySuccess(result) {
                console.log('call result: ' + result);
                console.log('Successfully verified');
                alert('Verification successful. You will now be redirected to the login page.');
        window.location.href = signinUrl;
            },
            function verifyError(err) {
                alert(err);
            }
        );
    }
}(jQuery));
