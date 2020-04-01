<?php

if(isset($_COOKIE['tg_user']) && isset($_GET['endpoint'])){
    $user_info = json_decode($_COOKIE['tg_user'], true);
    $user_id = $user_info['id'];
    $endpoint = $_GET['endpoint'];
}
else{
    header('Location: homepage.php');
}

$hostname = "http://watchlist:5001";
?>

<html>
    <body>
        <script>
        $(async () => {
            var hostname = '<?php echo $hostname; ?>';

            var userid = '<?php echo $user_id; ?>';
            var endpoint = '<?php echo $endpoint; ?>';
            // Change serviceURL to your own
            var serviceURL = hostname + ":5001/watchlist/remove";

            try {
                const response =
                await fetch(
                    serviceURL, {
                    method: 'POST',
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ id: userid, endpoint: endpoint})
                });
                
                const data = await response.json();
                var status = data.status;

                if (status != "success") {
                    var message = "Error in deletion, please try again.";
                    window.location.replace("homepage.php?status=error&message=" + message);
                } else {
                    var message = "Endpoint successfully deleted."
                    window.location.replace("homepage.php?status=success&message=" + message);
                }

            } catch (error) {
                var message = "Error connecting to the service, please try again later.";
                window.location.replace("homepage.php?status=error&message=" + message);
            }
        });
        </script>
    </body>
</html>