////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Cognito function written by me.
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*global Telemetry _config*/

var Telemetry = window.Telemetry || {};
Telemetry.map = Telemetry.map || {};

(function rideScopeWrapper($) {

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Confirmation form HTML being generated
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    function generateForm(email) {
        try {document.getElementById("emailForgotPasswordForm").innerHTML = "";}
        catch{}

        var form = document.getElementById("emailForgotPasswordForm");
        var header2 = document.createElement("h2");
        header2.innerText = "Enter your verification code and new password below."
        form.appendChild(header2)
        
        var newPasswordForm = document.createElement("form");
        newPasswordForm.id = "confirmNewPasswordForm"

        var verificationCodeInput = document.createElement("input");
        verificationCodeInput.id = "verificationCodeInput"
        verificationCodeInput.type = "text"
        verificationCodeInput.placeholder = "Verification code"
        verificationCodeInput.required = true

        var password1 = document.createElement("input");
        password1.id = "password1Input"
        password1.type = "password"
        password1.placeholder = "New password"
        password1.required = true
        password1.pattern = ".*"

        var password2 = document.createElement("input");
        password2.id = "password2Input"
        password2.type = "password"
        password2.placeholder = "Repeat new password"
        password2.required = true
        password2.pattern = ".*"

        var submitBtn = document.createElement("input");
        submitBtn.type = "submit"
        submitBtn.value = "Submit"

        newPasswordForm.appendChild(verificationCodeInput)
        newPasswordForm.appendChild(password1)
        newPasswordForm.appendChild(password2)
        newPasswordForm.appendChild(submitBtn)
        form.appendChild(newPasswordForm)

        $('#confirmNewPasswordForm').submit(function(e) {
            Telemetry.confirmResetPassword(email, event)
            e.preventDefault();
        });
    }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Page handlers etc
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // Register click handler for #request button
    $(function onDocReady() {
        $('#resetPasswordForm').submit(function(e) {
            var email = $('#emailInputSignin').val();
            Telemetry.resetPassword(event);
            e.preventDefault();
            generateForm(email);
        });
    });
}(jQuery));
