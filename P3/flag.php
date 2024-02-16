<?php
function generate_flag($user_id) {
    $flag_config = array(
        'prefix' => "nimda_KeYS_R0TaT1On_1s7_g0od_",
        'secret' => "client-decides-norway-twitch-expert-model",
        'salt_size' => 12
    );

    $PREFIX = $flag_config['prefix'];
    $SECRET = $flag_config['secret'];
    $SALT_SIZE = $flag_config['salt_size'];

    return $PREFIX . substr(hash_hmac("sha256", strval($user_id), $SECRET), 0, $SALT_SIZE);
}