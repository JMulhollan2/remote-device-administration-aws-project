/*global Telemetry _config*/

var Telemetry = window.Telemetry || {};
Telemetry.map = Telemetry.map || {};

(function rideScopeWrapper($) {
    var authToken;
    Telemetry.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = '/signin.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = '/signin.html';
    });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Functions for add device menu
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    function build_add_device_menu(apikey) {
        // Create menu
        var menu = document.createElement('div');
        menu.id = "addDeviceMenu"
        menu.className = "add-device-menu"

        // Bar for menu
        var add_device_nav_bar = document.createElement('ul');
        add_device_nav_bar.className = "nav-bar"
        add_device_nav_bar.id = "addDeviceNavBar"
        
        // Close button generation
        var close_button_li = document.createElement("li");
        close_button_li.id = "addDeviceCloseButton"
        close_button_li.style = "float:right";
        var close_button_a = document.createElement("a");
        close_button_a.className = "nav-bar-image-content";
        close_button_a.id = "closeMenu"
        close_button_a.href = "#"
        var close_button_img = document.createElement("img");
        close_button_img.src = "Close Logo 40.png"
        close_button_a.appendChild(close_button_img);
        close_button_li.appendChild(close_button_a);

        // Menu title
        var add_device_header = document.createElement('h2');
        add_device_header.className = "add-device-sub-title"
        var add_device_header_text = document.createTextNode("How to add a device:");
        add_device_header.appendChild(add_device_header_text)

        //Menu content
        var add_device_text_1 = document.createElement('h3');
        add_device_text_1.className = "add-device-text"
        var add_device_text_1_text = document.createTextNode("1. Download the desktop application.");
        add_device_text_1.appendChild(add_device_text_1_text)

        var add_device_text_2 = document.createElement('h3');
        add_device_text_2.className = "add-device-text"
        var add_device_text_2_text = document.createTextNode("2. Open the desktop application.");
        add_device_text_2.appendChild(add_device_text_2_text)

        var add_device_text_3 = document.createElement('h3');
        add_device_text_3.className = "add-device-text"
        var add_device_text_3_text = document.createTextNode("3. You will be prompted to input your account email and device key, found below.");
        add_device_text_3.appendChild(add_device_text_3_text)

        var add_device_text_4 = document.createElement('h4');
        add_device_text_4.className = "add-device-text"
        var add_device_text_4_text = document.createTextNode("By adding a device to your account, you agree to allowing your device to send location and device data to our servers.");
        add_device_text_4.appendChild(add_device_text_4_text)

        var api_key_box = document.createElement('input');
        api_key_box.className = 'add-device-input';
        api_key_box.id = "apiKeyBox"
        api_key_box.value = apikey
        api_key_box.readOnly = true

        var copy_button = document.createElement('button');
        copy_button.textContent = "Copy"
        copy_button.id = "copyButton"
        copy_button.className = "copy-button"

        // Append everything & publish
        add_device_nav_bar.appendChild(close_button_li);
        menu.appendChild(add_device_nav_bar);
        menu.appendChild(add_device_header);
        menu.appendChild(add_device_text_1);
        menu.appendChild(add_device_text_2);
        menu.appendChild(add_device_text_3);
        menu.appendChild(add_device_text_4);
        menu.appendChild(api_key_box);
        menu.appendChild(copy_button);
        document.body.appendChild(menu);

        // Give button purpose
        $('#addDeviceCloseButton').off('click').click(function() {
            var body = document.getElementById("addDeviceMenu");
            body.outerHTML = ""
            $('#addDeviceButton').off('click').click(function() {build_add_device_menu(apikey);});
        });
        // Edit account button switch between open/close
        $('#addDeviceButton').off('click').click(function() {
            var body = document.getElementById("addDeviceMenu");
            body.outerHTML = ""
            $('#addDeviceButton').off('click').click(function() {build_add_device_menu(apikey);});
        });
        $('#copyButton').off('click').click(function() {
            var copyText = document.getElementById("apiKeyBox");
            copyText.select();
            document.execCommand("copy");
        });
    }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Functions for edit account menu
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    function build_edit_account_menu() {
        // Create menu
        var menu = document.createElement('div');
        menu.id = "editAccountMenu"
        menu.className = "edit-account-menu"

        // Bar for menu
        var edit_account_nav_bar = document.createElement('ul');
        edit_account_nav_bar.className = "nav-bar"
        edit_account_nav_bar.id = "editAccountNavBar"
        
        // Close button generation
        var close_button_li = document.createElement("li");
        close_button_li.id = "editAccountCloseButton"
        close_button_li.style = "float:right";
        var close_button_a = document.createElement("a");
        close_button_a.className = "nav-bar-image-content";
        close_button_a.id = "closeMenu"
        close_button_a.href = "#"
        var close_button_img = document.createElement("img");
        close_button_img.src = "Close Logo 40.png"
        close_button_a.appendChild(close_button_img);
        close_button_li.appendChild(close_button_a);

        // Menu title
        var edit_account_header = document.createElement('h2');
        edit_account_header.className = "edit-account-sub-title"
        var edit_account_header_text = document.createTextNode("Edit account");
        edit_account_header.appendChild(edit_account_header_text)

        // Menu container
        var account_grid = document.createElement("div");
        account_grid.className = "editAccountGrid";

        // Change password
        var change_password_container = document.createElement("div");
        change_password_container.className = "changePasswordGrid"
        var change_password_title = document.createTextNode("Change password");
        change_password_title.className = "changePasswordTitle"
        change_password_container.appendChild(change_password_title);

        var change_password_form = document.createElement("form");
        change_password_form.id = "changePasswordForm"

        var old_password_input = document.createElement("input");
        old_password_input.id = "oldPasswordInputChangePassword";
        old_password_input.type = "password"
        old_password_input.placeholder = "Old password"
        old_password_input.required = true;
        change_password_form.appendChild(old_password_input)

        var new_password_input_1 = document.createElement("input");
        new_password_input_1.id = "newPasswordInput1ChangePassword";
        new_password_input_1.type = "password"
        new_password_input_1.placeholder = "New password"
        new_password_input_1.required = true;
        change_password_form.appendChild(new_password_input_1)

        var new_password_input_2 = document.createElement("input");
        new_password_input_2.id = "newPasswordInput2ChangePassword";
        new_password_input_2.type = "password"
        new_password_input_2.placeholder = "Repeat new password"
        new_password_input_2.required = true;
        change_password_form.appendChild(new_password_input_2)

        var submit_btn = document.createElement("input");
        submit_btn.type = "submit"
        submit_btn.value = "Reset password"
        change_password_form.appendChild(submit_btn)

        change_password_container.appendChild(change_password_form)
        account_grid.appendChild(change_password_container);

        // Append everything & publish
        edit_account_nav_bar.appendChild(close_button_li);
        menu.appendChild(edit_account_nav_bar);
        menu.appendChild(edit_account_header);
        menu.appendChild(account_grid);
        document.body.appendChild(menu);

        // Give button purpose
        $('#editAccountCloseButton').off('click').click(function() {
            var body = document.getElementById("editAccountMenu");
            body.outerHTML = ""
            $('#editAccount').off('click').click(function() {build_edit_account_menu();});
        });
        // Edit account button switch between open/close
        $('#editAccount').off('click').click(function() {
            var body = document.getElementById("editAccountMenu");
            body.outerHTML = ""
            $('#editAccount').off('click').click(function() {build_edit_account_menu();});
        });
        $('#changePasswordForm').submit(function() {
            Telemetry.changePassword(event);
        });
    }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Functions for building the singular device column
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // Update column itself
    function build_device_column(device_name, device_location, device_status, device_last_online, device_location_bool, device_sound_bool, device_platform, device_current_user, device_wipe_bool, device_logout_bool) {
        // Remove add button
        try {document.getElementById("addDeviceButton").outerHTML = "";}
        catch{}

        // Any data manipulation
        var device_name_data = device_name
        var device_location_data = device_location
        var device_status_data = device_status
        var device_last_online_data = device_last_online
        var device_platform_data = device_platform
        var device_current_user_data = device_current_user

        // Device time
        var parsed_time = Number(device_last_online_data)

        if (parsed_time.toString() != "NaN"){
            var time_since_seen = getTimeDifference(new Date(parsed_time))
        }
        else{
            var time_since_seen = "Unavailable"
        }

        // Set where data is to appended
        var body = document.getElementById("deviceList");
        body.innerHTML = ""

        //////////////////////////////////////////////////////
        // Update refresh button
        $('#refreshDevices').off('click').click(function() {getDeviceData(device_name);});

        // Dynamic bar for devices
        try {document.getElementById("deviceBackButton").outerHTML = "";}
        catch{}

        //////////////////////////////////////////////////////
        // Back button generation
        var device_bar = document.getElementById("deviceNavBar");
        var back_button_li = document.createElement("li");
        back_button_li.id = "deviceBackButton";
        var back_button_a = document.createElement("a");
        back_button_a.className = "nav-bar-image-content";
        back_button_a.id = "refreshDevices"
        back_button_a.href = "#"
        var back_button_img = document.createElement("img");
        back_button_img.src = "Back Logo 40.png"
        back_button_a.appendChild(back_button_img);
        back_button_li.appendChild(back_button_a);
        device_bar.appendChild(back_button_li)
        $('#deviceBackButton').click(function() {getUserData();});

        //////////////////////////////////////////////////////
        // Update map
        var map = document.getElementById('map')
        map.innerHTML = ""
        var device_location = JSON.parse(device_location)
        generate_single_map(device_name, device_location)

        //////////////////////////////////////////////////////
        // Build information grid
        var body = document.getElementById("deviceList");
        var grid = document.createElement("div");
        grid.className = "deviceInformation";

        // Create nformation grid
        let grid_item = document.createElement("div");
        grid_item.className = "deviceInformationGridContainer"
        grid_item.id = "singleDeviceInformationClick" // Probably not needed

        // Add information into grid
        var device_title_grid = document.createElement("div");
        device_title_grid.className = "deviceInformationNameGridTitle"
        var device_title = document.createTextNode(device_name_data);
        device_title.className = "deviceInformationNameTitle"
        device_title_grid.appendChild(device_title);
        grid_item.appendChild(device_title_grid);

        var device_status_grid = document.createElement("div");
        device_status_grid.className = "deviceInformationStatusGridTitle"
        var device_status = document.createTextNode(device_status_data);
        device_status.className = "deviceInformationStatusTitle"
        device_status_grid.appendChild(device_status);
        grid_item.appendChild(device_status_grid);

        var device_last_online_grid = document.createElement("div");
        device_last_online_grid.className = "deviceInformationLastOnlineGridTitle"
        var device_last_online = document.createTextNode("Last online: "+time_since_seen);
        device_last_online.className = "deviceInformationLastOnlineTitle"
        device_last_online_grid.appendChild(device_last_online);
        grid_item.appendChild(device_last_online_grid);

        var device_platform_grid = document.createElement("div");
        device_platform_grid.className = "deviceInformationPlatformGridTitle"
        var device_platform = document.createTextNode(device_platform_data);
        device_platform.className = "deviceInformationPlatformTitle"
        device_platform_grid.appendChild(device_platform);
        grid_item.appendChild(device_platform_grid);

        var device_user_grid = document.createElement("div");
        device_user_grid.className = "deviceInformationUserGridTitle"
        var device_user = document.createTextNode("Current user: "+device_current_user_data);
        device_user.className = "deviceInformationUserTitle"
        device_user_grid.appendChild(device_user);
        grid_item.appendChild(device_user_grid);

        // Append divs back to parent & publish
        grid.appendChild(grid_item)
        body.innerHTML = ""
        body.appendChild(grid);

        //////////////////////////////////////////////////////
        // Build device buttons
        var body = document.getElementById("deviceList");
        var grid = document.createElement("div");
        grid.className = "deviceButtons";

        // Create button grid
        let button_grid_item = document.createElement("div");
        button_grid_item.className = "buttonGridContainer"
        button_grid_item.id = "buttonDeviceClick" // Probably not needed

        // Add buttons into grid

        // Device refresh button
        var device_refresh_btn_grid = document.createElement("div");
        if (device_location_bool){
            device_refresh_btn_grid.className = "deviceRefreshBtnGridRequested"
            var device_refresh_btn = document.createTextNode("Data requested");
        }
        else{
            device_refresh_btn_grid.className = "deviceRefreshBtnGrid"
            var device_refresh_btn = document.createTextNode("Get data");
            device_refresh_btn_grid.onclick = function(){
                modify_table(device_name, "Device", "RemoteLocationEnabled", "True")
                setTimeout(function() {getDeviceData(device_name);}, 1200);
            }
        }
        device_refresh_btn.className = "deviceRefreshBtn"
        device_refresh_btn_grid.appendChild(device_refresh_btn);
        button_grid_item.appendChild(device_refresh_btn_grid);

        // Device sound button
        var device_sound_btn_grid = document.createElement("div");
        if (device_sound_bool){
            device_sound_btn_grid.className = "deviceSoundBtnGridRequested"
            var device_sound_btn = document.createTextNode("Sound requested");
        }
        else{
            device_sound_btn_grid.className = "deviceSoundBtnGrid"
            var device_sound_btn = document.createTextNode("Play sound");
            device_sound_btn_grid.onclick = function(){
                modify_table(device_name, "Device", "RemoteSoundEnabled", "True")
                setTimeout(function() {getDeviceData(device_name);}, 1400);
            }
        }
        device_sound_btn.className = "deviceSoundBtn"
        device_sound_btn_grid.appendChild(device_sound_btn);
        button_grid_item.appendChild(device_sound_btn_grid);

        // Delete device button
        var device_delete_btn_grid = document.createElement("div");
        device_delete_btn_grid.className = "deviceDeleteBtnGrid"
        var device_delete_btn = document.createTextNode("Delete device");
        device_delete_btn_grid.onclick = function(){
            var confirmBool = confirm("Are you sure you want to delete this device?");
            if (confirmBool == true) {
                delete_device(device_name);
                setTimeout(function() {getUserData();}, 1400);
            } else {
              console.log("User cancelled device delete")
            }
        }
        device_delete_btn.className = "deviceDeleteBtn"
        device_delete_btn_grid.appendChild(device_delete_btn);
        button_grid_item.appendChild(device_delete_btn_grid);

        // Device wipe button
        var device_wipe_btn_grid = document.createElement("div");
        if (device_wipe_bool){
            device_wipe_btn_grid.className = "deviceWipeBtnGridRequested"
            var device_wipe_btn = document.createTextNode("Wipe requested");
        }
        else{
            device_wipe_btn_grid.className = "deviceWipeBtnGrid"
            var device_wipe_btn = document.createTextNode("Wipe device");
            device_wipe_btn_grid.onclick = function(){
                var wipeConfirmBool = confirm("Are you sure you want to wipe this device's hard drive(s)? All data will not be recoverable.");
                if (wipeConfirmBool == true) {
                    modify_table(device_name, "Device", "RemoteWipeEnabled", "True")
                    setTimeout(function() {getDeviceData(device_name);}, 1400);
                } else {
                  console.log("User cancelled device wipe")
                }
            }
        }
        device_wipe_btn.className = "deviceWipeBtn"
        device_wipe_btn_grid.appendChild(device_wipe_btn);
        button_grid_item.appendChild(device_wipe_btn_grid);

        // Device logout button
        var device_logout_btn_grid = document.createElement("div");
        if (device_logout_bool){
            device_logout_btn_grid.className = "deviceLogoutBtnGridRequested"
            var device_logout_btn = document.createTextNode("Logout requested");
        }
        else{
            device_logout_btn_grid.className = "deviceLogoutBtnGrid"
            var device_logout_btn = document.createTextNode("Log out user");
            device_logout_btn_grid.onclick = function(){
                modify_table(device_name, "Device", "RemoteLogoutEnabled", "True")
                setTimeout(function() {getDeviceData(device_name);}, 1400);
            }
        }
        device_logout_btn.className = "deviceLogoutBtn"
        device_logout_btn_grid.appendChild(device_logout_btn);
        button_grid_item.appendChild(device_logout_btn_grid);

        // Append divs back to parent & publish
        grid.appendChild(button_grid_item)
        body.appendChild(grid);
    }

    // Generate the map
    function generate_single_map(device_name, device_location) {
        var myLatLng = {lat: device_location[0], lng: device_location[1]};
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: myLatLng
        });
        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: device_name
        });
    }

    // Parsing device data
    function parse_device_data(device_name, data){
        for (var device in data['AssignedDevices']['L']){
            if (device_name == data['AssignedDevices']['L'][device]['M']['DeviceName']['S']){
                var device_name = data['AssignedDevices']['L'][device]['M']['DeviceName']['S']
                var device_location = data['AssignedDevices']['L'][device]['M']['DeviceLocation']['S']
                var device_status = data['AssignedDevices']['L'][device]['M']['DeviceStatus']['S']
                var device_last_online = data['AssignedDevices']['L'][device]['M']['DeviceLastOnline']['S']
                var device_location_bool = data['AssignedDevices']['L'][device]['M']['RemoteLocationEnabled']['BOOL']
                var device_sound_bool= data['AssignedDevices']['L'][device]['M']['RemoteSoundEnabled']['BOOL']
                var device_platform = data['AssignedDevices']['L'][device]['M']['Platform']['S']
                var device_current_user = data['AssignedDevices']['L'][device]['M']['CurrentUser']['S']
                var device_wipe_bool = data['AssignedDevices']['L'][device]['M']['RemoteWipeEnabled']['BOOL']
                var device_logout_bool = data['AssignedDevices']['L'][device]['M']['RemoteLogoutEnabled']['BOOL']

                build_device_column(device_name, device_location, device_status, device_last_online, device_location_bool, device_sound_bool, device_platform, device_current_user, device_wipe_bool, device_logout_bool);
            }
        }
    }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Functions for displaying full devices list
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // Generate map for all devices
    function generate_multi_map(location_list) {
        var locations = location_list;
        var map = new google.maps.Map(document.getElementById('map'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP
          });
        var infowindow = new google.maps.InfoWindow();
        var marker, i;
        for (i = 0; i < locations.length; i++) {  
            marker = new google.maps.Marker({
              position: new google.maps.LatLng(locations[i][1], locations[i][2]),
              map: map
            });
      
            google.maps.event.addListener(marker, 'click', (function(marker, i) {
              return function() {
                infowindow.setContent(locations[i][0]);
                infowindow.open(map, marker);
              }
            })(marker, i));
        }
        //create empty LatLngBounds object
        var bounds = new google.maps.LatLngBounds();
        var infowindow = new google.maps.InfoWindow();    
        for (i = 0; i < locations.length; i++) {  
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
            map: map
        });
        //extend the bounds to include each marker's position
        bounds.extend(marker.position);
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
            infowindow.setContent(locations[i][0]);
            infowindow.open(map, marker);
            }
        })(marker, i));
        }
        //now fit the map to the newly inclusive bounds
        map.fitBounds(bounds);
    }

    // Generate list of all devices
    function generate_table(result, apikey) {
        // Remove buttons
        try {document.getElementById("deviceBackButton").outerHTML = "";}
        catch{}
        try {document.getElementById("addDeviceButton").outerHTML = "";}
        catch{}

        // Add add devices button
        var device_bar = document.getElementById("deviceNavBar");
        var add_button_li = document.createElement("li");
        add_button_li.id = "addDeviceButton";
        var add_button_a = document.createElement("a");
        add_button_a.className = "nav-bar-image-content";
        add_button_a.id = "addDevice"
        add_button_a.href = "#"
        var add_button_img = document.createElement("img");
        add_button_img.src = "Add Logo 40.png"
        add_button_a.appendChild(add_button_img);
        add_button_li.appendChild(add_button_a);
        device_bar.appendChild(add_button_li)
        $('#addDeviceButton').click(function() {build_add_device_menu(apikey);});


        // Get target body, creates encaspulating elements
        var body = document.getElementById("deviceList");
        var grid = document.createElement("div");
        grid.className = "devicesList";
        // Catches instance if there are no devices
        try{
            for (var device in result['AssignedDevices']['L']){
                let grid_item = document.createElement("div");
                grid_item.className = "devicesGridContainer";
                grid_item.id = "singleDeviceClick";
                grid_item.href = "#";

                let device_name = result['AssignedDevices']['L'][device]['M']['DeviceName']['S']
                let device_location = result['AssignedDevices']['L'][device]['M']['DeviceLocation']['S']
                let device_status = result['AssignedDevices']['L'][device]['M']['DeviceStatus']['S']
                let device_last_online = result['AssignedDevices']['L'][device]['M']['DeviceLastOnline']['S']
                let device_location_bool = result['AssignedDevices']['L'][device]['M']['RemoteLocationEnabled']['BOOL']
                let device_sound_bool= result['AssignedDevices']['L'][device]['M']['RemoteSoundEnabled']['BOOL']
                let device_platform = result['AssignedDevices']['L'][device]['M']['Platform']['S']
                let device_current_user = result['AssignedDevices']['L'][device]['M']['CurrentUser']['S']
                let device_wipe_bool = result['AssignedDevices']['L'][device]['M']['RemoteWipeEnabled']['BOOL']
                let device_logout_bool = result['AssignedDevices']['L'][device]['M']['RemoteLogoutEnabled']['BOOL']

                var parsed_time = Number(device_last_online)

                if (parsed_time.toString() != "NaN"){
                    var time_since_seen = getTimeDifference(new Date(parsed_time))
                }
                else{
                    var time_since_seen = "Device time unavailable"
                }

                grid_item.onclick = function(){build_device_column(device_name, device_location, device_status, device_last_online, device_location_bool, device_sound_bool, device_platform, device_current_user, device_wipe_bool, device_logout_bool)};

                var device_title_grid = document.createElement("div");
                device_title_grid.className = "deviceNameGridTitle"
                var device_title = document.createTextNode(device_name);
                device_title.className = "deviceNameTitle"
                device_title_grid.appendChild(device_title);
                grid_item.appendChild(device_title_grid);

                var device_status_grid = document.createElement("div");
                device_status_grid.className = "deviceStatusGridTitle"
                var device_status_div = document.createTextNode(device_status);
                device_status_div.className = "deviceStatusTitle"
                device_status_grid.appendChild(device_status_div);
                grid_item.appendChild(device_status_grid);

                var device_lastonline_grid = document.createElement("div");
                device_lastonline_grid.className = "deviceLastOnlineGridTitle"
                var device_lastonline = document.createTextNode(time_since_seen);
                device_lastonline.className = "deviceLastOnlineTitle"
                device_lastonline_grid.appendChild(device_lastonline);
                grid_item.appendChild(device_lastonline_grid);

                grid.appendChild(grid_item);
            }
        }
        catch(err){
            console.log(err)
        }
        // appends <table> into <body>
        body.innerHTML = ""
        body.appendChild(grid);
    }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Functions for building the page
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    function update_email(email) {
        document.getElementById("emailBtn").innerHTML = email;
    }

    function build_page(result) {
        //console.log(result); // Debug
        var email = result['Email']['S']
        var apikey = result['APIKey']['S']
        var location_list = []

        try{
            for (var device in result['AssignedDevices']['L']){
                var device_name = result['AssignedDevices']['L'][device]['M']['DeviceName']['S']
                var device_location = result['AssignedDevices']['L'][device]['M']['DeviceLocation']['S']
                if (device_location == "PlaceHolderValue"){
                    continue
                }
                else{
                    var device_location = JSON.parse(device_location)
                    device_location.unshift(device_name)
                    location_list.push(device_location)
                }
            }
        }
        catch{}

        update_email(email);
        generate_table(result, apikey);
        if (location_list.length == 0){
            try{
                document.getElementById("map").innerHTML = "";
            }
            catch{}

        }
        else {generate_multi_map(location_list);};
        $('#refreshDevices').off('click').click(function() {
            getUserData();
        });
        $('#editAccount').off('click').click(function() {build_edit_account_menu();});
    }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// API and math functions
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // Modify table API request
    function modify_table(DeviceName, DataType, AttributeToUpdate, UpdateValue) {
        $.ajax({
            method: 'POST',
            url: (_config.api.invokeUrl)+"update-table",
            headers: {
                Authorization: authToken,
                DeviceName: DeviceName,
                DataType: DataType,
                AttributeToUpdate: AttributeToUpdate,
                UpdateValue: UpdateValue,
            },
            contentType: 'application/json',
            //success: generate_table,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured:\n' + jqXHR.responseText);
                location.reload();
            }
        });
    }

    // Delete table API request
    function delete_device(DeviceName) {
        $.ajax({
            method: 'POST',
            url: (_config.api.invokeUrl)+"update-table",
            headers: {
                Authorization: authToken,
                DeviceName: DeviceName,
                DeleteDeviceBool: "True",
            },
            contentType: 'application/json',
            //success: generate_table,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured:\n' + jqXHR.responseText);
                location.reload();
            }
        });
    }

    // Get all user data
    function getUserData() {
        $.ajax({
            method: 'GET',
            url: _config.api.invokeUrl,
            headers: {
                Authorization: authToken
            },
            contentType: 'application/json',
            success: build_page,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured:\n' + jqXHR.responseText);
                location.reload();
            }
        });
    }

    // Get all user data WITH DEVICE attribute (used for pulling specific device data)
    function getDeviceData(device_name) {
        $.ajax({
            method: 'GET',
            url: _config.api.invokeUrl,
            headers: {
                Authorization: authToken
            },
            contentType: 'application/json',
            success:function(data) {
                parse_device_data(device_name, data); 
            },
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured:\n' + jqXHR.responseText);
                location.reload();
            }
        });
    }

    // Calculate time
    function getTimeDifference(date) {
        var seconds = Math.floor((new Date() - date) / 1000);

        var interval = Math.floor(seconds / 31536000);
      
        if (interval > 1) {
          return interval + " years ago";
        }
        interval = Math.floor(seconds / 2592000);
        if (interval > 1) {
          return interval + " months ago";
        }
        interval = Math.floor(seconds / 86400);
        if (interval > 1) {
          return interval + " days ago";
        }
        interval = Math.floor(seconds / 3600);
        if (interval > 1) {
          return interval + " hours ago";
        }
        interval = Math.floor(seconds / 60);
        if (interval > 1) {
          return interval + " minutes ago";
        }
        return Math.floor(seconds) + " seconds ago";
    }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Page handlers etc
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    function updatePage(result) {
        displayUpdate('User details returned.');
        console.log(result)
        $('.userApiData').text(JSON.stringify(result))
    }

    // Register click handler for #request button
    $(function onDocReady() {
        $('#signOut').click(function() {
            Telemetry.signOut();
            alert("You have been signed out.");
            window.location = "signin.html";
        });

        Telemetry.authToken.then(function updateAuthMessage(token) {
            if (token) {
                displayUpdate('You are authenticated.');
                $('.authToken').text(token);
                getUserData();
            }
        });
    });

    function displayUpdate(text) {
        $('#updates').append($('<li>' + text + '</li>'));
    }
}(jQuery));
