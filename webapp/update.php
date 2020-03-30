<?php
define('BOT_USERNAME', '@ESD_Proj_bot'); // place username of your bot here

if (isset($_COOKIE['tg_user'])) {
	$user_info = json_decode($_COOKIE['tg_user'], true);
	$user_id = $user_info['id'];
	$first_name = $user_info['first_name'];
	$photo_url = $user_info['photo_url'];
}

if (isset($_GET['endpoint']) && isset($_GET['contacts'])) {
    $endpoint = $_GET['endpoint'];
    $contacts = $_GET['contacts'];
}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!--
Design by TEMPLATED
http://templated.co
Released for free under the Creative Commons Attribution License

Name       : Skeleton 
Description: A two-column, fixed-width design with dark color scheme.
Version    : 1.0
Released   : 20130902

-->
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>G5T6 Watchdog Application</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />

    <link rel="icon" type="image/png" href="images/icons/favicon.ico" />
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="src/tables/vendor/bootstrap/css/bootstrap.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="src/tables/fonts/font-awesome-4.7.0/css/font-awesome.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="src/tables/vendor/animate/animate.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="src/tables/vendor/select2/select2.min.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="src/tables/vendor/perfect-scrollbar/perfect-scrollbar.css">
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="src/tables/css/util.css">
    <link rel="stylesheet" type="text/css" href="src/tables/css/main.css">

    <link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet" />
    <link href="src/default.css" rel="stylesheet" type="text/css" media="all" />
    <link href="src/fonts.css" rel="stylesheet" type="text/css" media="all" />

    <!--[if IE 6]><link href="default_ie6.css" rel="stylesheet" type="text/css" /><![endif]-->

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>

</head>

<body>
    <div id="page" class="container">
        <div id="header">
            <div id="logo">
                <img width="100px" src="<?= $photo_url ?>" alt="" />
                <h1 style="color:#6c7ae0"><?= $first_name ?></a></h1>
                <span>Welcome!</span>
            </div>
            <div id="menu">
                <ul>
                    <li class="current_page_item"><a href="homepage.php" accesskey="1" title="">Homepage</a></li>
                    <li><a href="add-endpoint.php" accesskey="2" title="">Add Endpoint</a></li>
                    <li><a href="logout.php" accesskey="3" title="">Log Out</a></li>
                </ul>
            </div>
        </div>
        <div id="main">
            <div id="welcome">
                <div class="title">
                    <h2>G5T6 Watchdog Application</h2>
                    <span class="byline">Monitor your websites with ease</span>
                </div>
                <p>Edit your of list websites <strong>below!</strong></p>
            </div>
            <div id="featured">
                <div class="title">
                    <h2>Edit</h2>
                </div>

                <p id="main-container"></p>

                <div class="limiter">
                    <div class="container-table100">
                        <div class="wrap-table100">
                            <div class="table100 ver1 m-b-110">
                                <div class="table100-head">
                                    <table align="center">
                                        <thead>
                                            <tr class="row100 head">
                                                <th class="cell100 t1column1">Website</th>
                                                <th class="cell100 t1column2">Chat Group</th>
                                            </tr>
                                        </thead>
                                    </table>
                                </div>
                                <div class="table100-body js-pscroll">
                                    <form id='updateEndpoint'>
                                        <table id="updateTable">
                                            <tbody>

                                            </tbody>
                                        </table>
                                    </form </div> </div> </div> </div> </div> </div> <div id="copyright">
                                    <span>&copy; Untitled. All rights reserved. | Application By G5T6'2020</span>
                                    <span>Design by <a href="http://templated.co" rel="nofollow">TEMPLATED</a>.</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Helper function to display error message
        function showError(message) {
            // Hide the table and button in the event of error
            // $('#endpointTable').hide();

            // Display an error under the main container
            $('#main-container')
                .append("<label>" + message + "</label>");
        }

        $(async () => {

            var userid = '<?php echo $user_id; ?>';
            var endpoint = '<?php echo $endpoint; ?>';
            var old_contacts = <?php echo $contacts; ?>;
            // Change serviceURL to your own
            var serviceURL = "http://esdwatchdog:5000/contact/get/" + userid;

            try {
                const response =
                    await fetch(
                        serviceURL, {
                        method: 'GET',
                        });

                const data = await response.json();
                var status = data.status;

                if (status != "success") {
                    showError(data.message);
                } else {
                    var allcontacts = data.result;
                    // for loop to setup all table rows with obtained contacts data
                    var row = "<tr class='row100 body'>" +
                        "<td class='cell100 t2column1' style='width:15em; text-align:left'>" + endpoint + "</td>" +
                        "<form id='updateEndpoint'><td class='cell100 t2column2' style='width:12em'>" +
                        "<select id='chats' name='chats' multiple>";

                    for (const c of allcontacts) {
                        if (c.chatid in old_contacts) {
                            row += "<option value='" + c.chat_id + "' selected>" + c.chat_title + "</option>";
                        } else {
                            row += "<option value='" + c.chat_id + "'>" + c.chat_title + "</option>";
                        }
                    }

                    row += "</select></td>" +
                        "<td class='cell100 t2column3' style='width:7em'><input id='updateBtn' class='btn btn-primary' type='submit' value='Add'></td></form></tr>";


                    // add all the rows to the table
                    $('#updateTable tbody').append(row);
                }
            } catch (error) {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                showError
                    ('There is a problem retrieving data, please try again later.<br />');

            } // error
        });

        $('#updateEndpoint').submit(async (event) => {

            var userid = '<?php echo $user_id; ?>';
            var endpoint = '<?php echo $endpoint; ?>';
            var old_contacts = <?php echo $contacts; ?>;
            // GET SELECTED CHAT GROUP'S CHAT ID
            var new_contacts = $('#chats').val();

            // Change serviceURL to your own
            var serviceURL = "http://esdwatchdog:5000/watchlist/update";


            try {
                const response =
                    await fetch(
                        serviceURL, {
                            method: 'PATCH',
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                userID: userid,
                                endpoint: endpoint,
                                old_chat_id: old_contacts,
                                new_chat_id: new_contacts
                            })
                        });

                const data = await response.json();
                // console.log(data);
                if (status != "success") {
                    window.location.replace("homepage.php?error");
                } else {
                    window.location.replace("homepage.php?success");
                }

            } catch (error) {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                window.location.replace("homepage.php?error");

            } // error
        });
    </script>
</body>

</html>