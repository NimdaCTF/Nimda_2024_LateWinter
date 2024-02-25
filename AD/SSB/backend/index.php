<?php

error_reporting(E_ERROR | E_PARSE);

require_once 'source/database.php';
require_once 'source/auth.php';
require_once 'source/utils.php';
require_once 'source/user.php';
require_once 'source/rating.php';

// Yep, I know. But that is my old project from ~2020 xd.
// Dont like php btw

ini_set("session.gc_maxlifetime", 3600);

session_start();
// Actually, I don't remember for what I added it
header("Access-Control-Allow-Origin: http://localhost");
header("Access-Control-Expose-Headers: Content-Length, X-JSON");
header("Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
header("Access-Control-Allow-Credentials: true");

mkdir('./tmp');

$db_methods = new DataBase();
$user_methods = new User();
$rating_methods = new Rating();

if (isset($_GET['method'])) {
    switch ($_GET['method']) {
        case 'getInstitutesList':
            echo generate_true_callback($db_methods->getInstitutesList());
            break;
        case 'getGroupsByInstitute':
            if (isset($_GET['institute_id'])) {
                echo generate_true_callback($db_methods->getGroupByInstitute($_GET['institute_id']));
                break;
            }
            die(generate_error_callback('Invalid institute_id'));
        case 'getStudentsByGroup':
            if (isset($_GET['group_id'])) {
                echo generate_true_callback($db_methods->getStudentsByGroup($_GET['group_id']));
                break;
            }
            die(generate_error_callback('Invalid group_id'));
        case 'getUser':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                echo $user_methods->getUser();
                break;
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getGroupRating':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                echo $rating_methods->getGroupRating();
                break;
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getGlobalRating':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                echo $rating_methods->getGlobalRating();
                break;
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getGroupSubjects':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                echo $user_methods->getSubjects();
                break;
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getStudentMarks':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                echo $user_methods->getMarks();
                break;
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getCurrentSubjects':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                if (isset($_GET['semester'])) {
                    echo generate_true_callback($db_methods->getCurrentSubjects($_SESSION['id'], $_GET['semester']));
                    break;
                } else
                    die(generate_error_callback('Semester was empty'));
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getTeacherByCourseId':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                if (isset($_GET['id'])) {
                    echo generate_true_callback($db_methods->getTeacherBySubjectId($_GET['id']));
                    break;
                } else
                    die(generate_error_callback('Id was empty'));
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getSubjectById':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                if (isset($_GET['id'])) {
                    echo generate_true_callback($db_methods->getSubjectById($_GET['id']));
                    break;
                } else
                    die(generate_error_callback('Id was empty'));
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getTasksBySubject':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                if (isset($_GET['id'])) {
                    echo generate_true_callback($db_methods->getTasksForSubject($_GET['id']));
                    break;
                } else
                    die(generate_error_callback('Id was empty'));
            }
            die(generate_error_callback('Not authorized', 401));
        case 'getTaskById':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                if (isset($_GET['id'])) {
                    echo generate_true_callback($db_methods->getTaskById($_GET['id'], $_SESSION['id']));
                    break;
                } else
                    die(generate_error_callback('Id was empty'));
            }
            die(generate_error_callback('Not authorized', 401));
        case 'loadFile':
            if (isset($_SESSION['status']) && $_SESSION['status']) {
                if (isset($_GET['id'])) {
                    $file = $db_methods->loadFile($_GET['id'], $_SESSION['id']);
                    $filename = './tmp/' . $file[1];
                    file_put_contents($filename, $file[0]);


                    $finfo = finfo_open(FILEINFO_MIME_TYPE);
                    header('Content-Type: ' . finfo_file($finfo, $filename));
                    finfo_close($finfo);

                    header('Content-Disposition: inline; filename=' . basename($filename));

                    header('Expires: 0');
                    header('Cache-Control: must-revalidate');
                    header('Pragma: public');

                    header('Content-Length: ' . filesize($filename));

                    ob_clean();
                    flush();
                    echo file_get_contents($filename);

                    break;
                }
                else if (isset($_GET['filename'])) {
                    $filename = $_GET['filename']; 

                    if (!preg_match('/^[a-zA-Z0-9_.-]+$/', $filename)) {
                        die("Invalid filename"); 
                    }

                    $filename = './tmp/' . basename($filename); 
                    
                    echo file_get_contents($filename);
                    break;
                }
                else
                    die(generate_error_callback('Id was empty'));
            }
            die(generate_error_callback('Not authorized', 401));
        default:
            die(generate_error_callback('Invalid method'));

    }
} else {
    $data = file_get_contents('php://input');
    if ($data) {
        $data = json_decode($data, JSON_UNESCAPED_UNICODE);
        if (isset($data['method'])) {
            $auth = new Authorization();
            switch ($data['method']) {
                case 'auth':
                    if ($auth->isAuthed()) {
                        echo generate_true_callback(array(
                            'status' => $_SESSION['status'],
                            'id' => $_SESSION['id'],
                            'username' => $_SESSION['username']
                        ));
                        return;
                    }
                    if (isset($data['auth_type'])) {
                        if ($data['auth_type'] === 'institute') {
                            if (isset($data['password']) && isset($data['id']))
                                echo $auth->auth('institute', $data['password'], null, $data['id']);
                            else
                                die(generate_error_callback('Empty password and(or) id passed'));
                        } elseif ($data['auth_type'] === 'special') {
                            if (isset($data['password']) && isset($data['username'])) {
                                echo $auth->auth('special', $data['password'], strtolower($data['username']), null);
                            } else
                                die(generate_error_callback('Empty password and(or) id passed'));
                        }
                    } else
                        die(generate_error_callback('Specify auth type'));
                    break;
                case 'logout':
                    echo $auth->logout();
                    break;
                case 'signup':
                    if ($auth->isAuthed()) {
                        echo generate_true_callback(array(
                            'status' => $_SESSION['status'],
                            'id' => $_SESSION['id'],
                            'username' => $_SESSION['username']
                        ));
                        return;
                    }
                    if (isset($data['signup_type'])) {
                        if ($data['signup_type'] === 'institute') {
                            if (isset($data['surname']) && isset($data['name']) && isset($data['patronymic']) && isset($data['password']))
                                echo $auth->signup($data['surname'], $data['name'], $data['patronymic'], null, $data['password'], 'institute');
                            else
                                die(generate_error_callback('Invalid fields passed'));
                        } elseif ($data['signup_type'] === 'special') {
                            if (isset($data['password']) && isset($data['username']))
                                echo $auth->signup(null, null, null, strtolower($data['username']), $data['password'], 'special');
                            else
                                die(generate_error_callback('Invalid fields passed'));
                        } elseif ($data['signup_type'] === 'full') {
                            if (isset($data['username']) && isset($data['surname']) && isset($data['name']) && isset($data['patronymic']) && isset($data['password']))
                                echo $auth->signup($data['surname'], $data['name'], $data['patronymic'], strtolower($data['username']), $data['password'], 'full');
                            else
                                die(generate_error_callback('Invalid fields passed'));
                        }
                    } else
                        die(generate_error_callback('Specify auth type'));
                    break;
                case 'updatePassword':
                    if (isset($_SESSION['status']) && $_SESSION['status']) {
                        if (empty($data['password']))
                            die(generate_error_callback('Empty password passed'));

                        echo $auth->updatePassword($data['password']);
                        break;
                    }
                    die(generate_error_callback('Not authed', 401));

                case 'updateSecret':
                    if (isset($_SESSION['status']) && $_SESSION['status']) {
                        if (empty($data['newSecret']))
                            die(generate_error_callback('Empty newSecret passed'));

                        echo $user_methods->setSecret($data['newSecret']);
                        break;
                    }
                    die(generate_error_callback('Not authed', 401));
                case 'uploadFile':
                    if (isset($_SESSION['status']) && $_SESSION['status']) {
                        if (empty($data['file']) || empty($data['taskId']) || empty($data['filename']))
                            die(generate_error_callback('Empty taskId or file or filename passed'));

                        echo $user_methods->uploadFile($data['taskId'], $data['file'], $data['filename']);
                        break;
                    }
                    die(generate_error_callback('Not authed', 401));
                case 'initUser':
                    if (isset($_SESSION['status']) && $_SESSION['status']) {
                        if (empty($data['snp']) || empty($data['group_id']))
                            die(generate_error_callback('Empty snp or group_id passed'));

                        echo $user_methods->init($data['group_id'], $data['snp']);
                        break;
                    }
                    die(generate_error_callback('Not authed', 401));

            }
        } else
            die(generate_error_callback('Invalid request', 404));
    } else
        die(generate_error_callback('Invalid request', 404));
}
