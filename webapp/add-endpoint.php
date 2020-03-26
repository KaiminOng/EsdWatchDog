<?php
define('BOT_USERNAME', '@ESD_Proj_bot'); // place username of your bot here

// var_dump($_COOKIE);

if (isset($_COOKIE['tg_user'])){
  $user_info = json_decode($_COOKIE['tg_user'], true);
  // print_r($_COOKIE['tg_user']);
  $user_id = $user_info['id'];
//   echo "USER ID:".$user_info['id'];
}

function getTelegramUserData() {
  if (isset($_COOKIE['tg_user'])) {
    $auth_data_json = urldecode($_COOKIE['tg_user']);
    $auth_data = json_decode($auth_data_json, true);
    return $auth_data;
  }
  return false;
}

$tg_user = getTelegramUserData();
if ($tg_user !== false) {
  // var_dump($tg_user);
  $first_name = $tg_user['first_name'];

  if (isset($tg_user['last_name'])){
    $last_name = " ".$tg_user['last_name'];
  } else{
    $last_name = "";
  }

  if (isset($tg_user['photo_url'])) {
    $photo_url = $tg_user['photo_url'];
  }
}
?>

<html>

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="src/css/bootstrap.min.css" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="src/css/dashboard.css" rel="stylesheet">

    <Title>WatchDog Dashboard</Title>

    <style>
        .status-active {
            color: #28a745;
            font-weight: bold
        }

        .status-inactive {
            color: #ff0000;
            font-weight: bold
        }

        .th-custom {

            font-size: large;
            text-align: center;

        }

        .td-custom {

            font-size: large;
            text-align: center;

        }

        .PerformanceTable {
            table-layout: fixed;
        }

        .PerformanceCell {
            height: 103.2px;
            overflow: hidden;
            width: 25%;
        }
    </style>

    <script 
    src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    
    <script
    src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"
    integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut"
    crossorigin="anonymous"></script>
    
    <script 
    src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"
    integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k"
    crossorigin="anonymous"></script>
</head>

<body>
    <nav class="navbar navbar-dark fixed-top bg-primary flex-md-nowrap p-0 shadow">
        <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="watchlist.php">WATCHDOG APPLICATION</a>
        <ul class="navbar-nav px-3">
            <li class="nav-item text-nowrap">
                <a class="nav-link" href="logout.php">Sign out</a>
            </li>
        </ul>
    </nav>

    <div class="container-fluid">
        <div class="row">
            <nav class="col-md-2 d-none d-md-block bg-light sidebar">
                <div class="sidebar-sticky">
                    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                        <span>Functions</span>
                        <a class="d-flex align-items-center text-muted" href="#">
                            <span data-feather="plus-circle"></span>
                        </a>
                    </h6>
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link" href="dashboard.php">
                                Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="add-endpoint.php">
                                Add Endpoint <span class="sr-only">(current)</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">
                                #####
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>

            <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <table>
                        <tr>
                            <td width='850px'>
                                <h1 class="h2">Add Endpoint</h1>
                            </td>
                            <td class='text-capitalize'>
                                
                            </td>
                            <td width='700px'></td>
                            <td>
                                <h4 style="width:max-content">Welcome, <?= $first_name.$last_name?>!</h4>
                            </td>
                        </tr>
                    </table>
                </div>
                <div class='mt-5'>
                    <a href=dashboard.php role="button" class="btn btn-primary">Back</a>
                    <table class='table table-bordered table-hover mt-4 col-10'>
                        <thead class='thead-light'>
                            <tr>
                                <th>Endpoint</th>
                                <th>Chat Group</th>
                                <th>Contact Type?</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class='text-center'><input name="endpoint" type="text" id="endpoint"></td>
                                <td>TO PLACE DROPDOWN LIST OF CHATS</td>
                                <td>TYPE???</td>
                                <td class='text-center'><input id='addBtn' class='btn btn-primary' type='submit' value='Add'></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
    <script>
    </script>
    <script src="src/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" crossorigin="anonymous"></script>
    <script src="src/js/bootstrap.bundle.js" crossorigin="anonymous"></script>

    <script>
        // Helper function to display error message
        function showError(message) {
            // Hide the table and button in the event of error
            // $('#endpointTable').hide();
    
            // Display an error under the main container
            $('#main-container')
                .append("<label>"+message+"</label>");
        }
    
        // anonymous async function 
        // - using await requires the function that calls it to be async
        $('#addBtn').click(async (event) => {          

            var userid = '<?php echo $user_id; ?>';

            var endpoint = $('#title').val();
            // GET SELECTED CHAT GROUP'S CHAT ID
            // var chatid = ????

            // Change serviceURL to your own
            var serviceURL = "http://esdwatchdog:5000/endpoint/new";
    
            try {
                const response =
                await fetch(
                    serviceURL, {
                    method: 'POST',
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ userID: userid, endpoint: endpoint, 
                        chatID: chatid})
                });

                const data = await response.json();
                // console.log(data);
                if (data[1] === 400){
                    document.getElementById("message").innerHTML = data[0].message
                }
                else if(data[1] === 201){
                    document.getElementById("message").innerHTML = title + " has been succesfully added."
                }

            } catch (error) {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                showError
            ('There is a problem adding the endpoint, please try again later.<br />'+error);
            
            } // error
        });
    </script>

    

</body>
</html>