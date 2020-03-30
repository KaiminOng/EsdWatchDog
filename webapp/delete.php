<?php

if(isset($_COOKIE['tg_user']) && isset($_GET['endpoint'])){
    $user_info = json_decode($_COOKIE['tg_user'], true);
    $user_id = $user_info['id'];
    $endpoint = $_GET['endpoint'];
}
else{
    header('Location: homepage.php');
}

?>

<html>
    <body>
        <script>
        $(async () => {

            var userid = '<?php echo $user_id; ?>';
            var endpoint = '<?php echo $endpoint; ?>';
            // Change serviceURL to your own
            var serviceURL = "http://esdwatchdog:5001/watchlist/remove";

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
                    window.location.replace("homepage.php?error");
                } else {
                    window.location.replace("homepage.php?success");                    
                }
            } catch (error) {
                window.location.replace("homepage.php?error");
            }
        });
        </script>
    </body>
</html>