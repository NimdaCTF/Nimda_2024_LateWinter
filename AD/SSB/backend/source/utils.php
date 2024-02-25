<?php
function generate_error_callback($error, $code = 400)
{
    http_response_code($code);
    return json_encode(array('status' => false, 'error' => $error), JSON_UNESCAPED_UNICODE);
}

function generate_true_callback($data = array(), $code = 200)
{
    http_response_code($code);
    return json_encode(array_merge(array('status' => true), $data), JSON_UNESCAPED_UNICODE);
}
