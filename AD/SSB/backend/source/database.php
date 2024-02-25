<?php

use SQLite3;

class DataBase
{
    private $conn = null;

    public function __construct()
    {
        $this->conn = new SQLite3("px.db") or die('database down');
        // $this->initDb();
    }

    private function initDb()
    {
        $this->conn->exec('CREATE TABLE IF NOT EXISTS institutes (id INTEGER PRIMARY KEY, name TEXT unique);');
        $this->conn->exec('CREATE TABLE IF NOT EXISTS groups     (id INTEGER PRIMARY KEY, name TEXT unique, i_id INTEGER, FOREIGN KEY (i_id) REFERENCES institutes(id));');
        $this->conn->exec('CREATE TABLE IF NOT EXISTS students   (id INTEGER PRIMARY KEY, surname TEXT NOT NULL DEFAULT "", name TEXT NOT NULL DEFAULT "", patronymic TEXT NOT NULL DEFAULT "", username TEXT DEFAULT NULL, password TEXT, group_id INTEGER, FOREIGN KEY (group_id) REFERENCES groups(id));');
        $this->conn->exec('CREATE TABLE IF NOT EXISTS teachers   (id INTEGER PRIMARY KEY, surname TEXT NOT NULL DEFAULT "", name TEXT NOT NULL DEFAULT "", patronymic TEXT NOT NULL DEFAULT "", username TEXT DEFAULT NULL, password TEXT);');
        $this->conn->exec('CREATE TABLE IF NOT EXISTS marks      (id INTEGER PRIMARY KEY, subject_id INTEGER NOT NULL, mark TEXT NOT NULL, student_id INTEGER NOT NULL, event INTEGER NOT NULL, FOREIGN KEY (student_id) REFERENCES students(id), FOREIGN KEY (subject_id) REFERENCES subjects(id));');
        $this->conn->exec('CREATE TABLE IF NOT EXISTS subjects   (id INTEGER PRIMARY KEY, name TEXT NOT NULL, group_id INTEGER NOT NULL, host_id INTEGER NOT NULL, semester INTEGER NOT NULL, pass_type TEXT NOT NULL, FOREIGN KEY (host_id) REFERENCES teachers(id), FOREIGN KEY (group_id) REFERENCES groups(id));');
        $this->conn->exec('CREATE TABLE IF NOT EXISTS tasks      (id INTEGER PRIMARY KEY, title TEXT NOT NULL, body TEXT not null default "", answer TEXT null, filename TEXT null, subject_id INTEGER not null, is_closed boolean not null default false, FOREIGN KEY (subject_id) REFERENCES subjects(id));');
    }

    public function getInstitutesList()
    {
        $result = $this->conn->query("SELECT * FROM institutes;") or die('Something went wrong');
        $tmp = array();
        while ($_ = $result->fetchArray(SQLITE3_ASSOC))
            array_push($tmp, $_);
        return array('values' => $tmp);
    }

    public function getGroupByInstitute($institute_id)
    {
        $stmt = $this->conn->prepare("SELECT * FROM groups WHERE i_id=:id;");
        $stmt->bindParam(':id', $institute_id, SQLITE3_INTEGER);
        $result = $stmt->execute();

        $tmp = array();
        while ($_ = $result->fetchArray(SQLITE3_ASSOC))
            array_push($tmp, $_);
        return array('values' => $tmp);
    }

    public function getStudentsByGroup($group_id)
    {
        $stmt = $this->conn->prepare("SELECT id, name, surname, patronymic, username FROM students WHERE group_id=:id;");
        $stmt->bindParam(':id', $group_id, SQLITE3_INTEGER);
        $result = $stmt->execute();

        $tmp = array();
        while ($_ = $result->fetchArray(SQLITE3_ASSOC))
            array_push($tmp, $_);
        return array('values' => $tmp);
    }

    public function isUserExists($id = null, $username = null)
    {
        $stmt = '';

        if (!is_null($id)) {
            $stmt = $this->conn->prepare("SELECT id FROM students WHERE id=:id;");
            $stmt->bindParam(':id', $id, SQLITE3_INTEGER);
        }
        if (!is_null($username)) {
            $stmt = $this->conn->prepare("SELECT id FROM students WHERE username=:username;");
            $stmt->bindParam(':username', $username, SQLITE3_TEXT);
        }

        if ($stmt !== '') {
            $result = $stmt->execute();
            return !empty($result->fetchArray(SQLITE3_ASSOC));
        }

        return null;
    }

    public function getStudent($id = null, $username = null)
    {
        $stmt = null;
        if ($id) {
            $stmt = $this->conn->prepare("SELECT * FROM students WHERE id=:id;");
            $stmt->bindParam(':id', $id, SQLITE3_INTEGER);
        }
        if ($username) {
            $stmt = $this->conn->prepare("SELECT * FROM students WHERE username=:username;");
            $stmt->bindParam(':username', $username, SQLITE3_TEXT);
        }

        if ($stmt) {
            $result = $stmt->execute();
            return $result->fetchArray(SQLITE3_ASSOC);
        }

        return null;
    }

    public function updateSNP($surname, $name, $patronymic, $id)
    {
        $stmt = $this->conn->prepare("UPDATE students SET surname=:surname, name=:name, patronymic=:patronymic WHERE id=:id");
        $stmt->bindParam(':surname', $surname, SQLITE3_TEXT);
        $stmt->bindParam(':name', $name, SQLITE3_TEXT);
        $stmt->bindParam(':patronymic', $patronymic, SQLITE3_TEXT);
        $stmt->bindParam(':id', $id, SQLITE3_INTEGER);
        $stmt->execute();
    }

    public function addUserSpecial($username, $password)
    {
        $stmt = $this->conn->prepare("INSERT INTO students (username, password) VALUES (:username, :password)");
        $stmt->bindParam(':username', $username, SQLITE3_TEXT);
        $stmt->bindParam(':password', $password, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function addUserInstitute($surname, $name, $patronymic, $password)
    {
        $stmt = $this->conn->prepare("INSERT INTO students (surname, name, patronymic, password) VALUES (:surname, :name, :patronymic, :password)");
        $stmt->bindParam(':surname', $surname, SQLITE3_TEXT);
        $stmt->bindParam(':name', $name, SQLITE3_TEXT);
        $stmt->bindParam(':patronymic', $patronymic, SQLITE3_TEXT);
        $stmt->bindParam(':password', $password, SQLITE3_TEXT);
        $stmt->execute();

    }

    public function addUserFull($surname, $name, $patronymic, $username, $password)
    {
        $stmt = $this->conn->prepare("INSERT INTO students (surname, name, patronymic, username, password) VALUES (:surname, :name, :patronymic, :username, :password)");
        $stmt->bindParam(':surname', $surname, SQLITE3_TEXT);
        $stmt->bindParam(':name', $name, SQLITE3_TEXT);
        $stmt->bindParam(':patronymic', $patronymic, SQLITE3_TEXT);
        $stmt->bindParam(':username', $username, SQLITE3_TEXT);
        $stmt->bindParam(':password', $password, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function updatePassword($student_id, $password)
    {
        $stmt = $this->conn->prepare("UPDATE students SET password=:password WHERE id=:sid;");
        $stmt->bindParam(':password', $password, SQLITE3_TEXT);
        $stmt->bindParam(':sid', $student_id, SQLITE3_INTEGER);
        $stmt->execute();
    }

    public function getTeacher($id = null, $username = null)
    {
        $result = null;
        if ($id) {
            $stmt = $this->conn->prepare("SELECT * FROM teachers WHERE id=:id;");
            $stmt->bindParam(':id', $id, SQLITE3_INTEGER);
            $result = $stmt->execute();
        }
        if ($username) {
            $stmt = $this->conn->prepare("SELECT * FROM teachers WHERE username=:username;");
            $stmt->bindParam(':username', $username, SQLITE3_TEXT);
            $result = $stmt->execute();
        }


        return $result?->fetchArray(SQLITE3_ASSOC);
    }

    public function addTeacherSpecial($username, $password)
    {
        $stmt = $this->conn->prepare("INSERT INTO teachers (username, password) VALUES (:username, :password)");
        $stmt->bindParam(':username', $username, SQLITE3_TEXT);
        $stmt->bindParam(':password', $password, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function addTeacherInstitute($surname, $name, $patronymic, $password)
    {
        $stmt = $this->conn->prepare("INSERT INTO teachers (surname, name, patronymic, password) VALUES (:surname, :name, :patronymic, :password)");
        $stmt->bindParam(':surname', $surname, SQLITE3_TEXT);
        $stmt->bindParam(':name', $name, SQLITE3_TEXT);
        $stmt->bindParam(':patronymic', $patronymic, SQLITE3_TEXT);
        $stmt->bindParam(':password', $password, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function addTeacherFull($surname, $name, $patronymic, $username, $password)
    {
        $stmt = $this->conn->prepare("INSERT INTO teachers (surname, name, patronymic, username, password) VALUES (:surname, :name, :patronymic, :username, :password)");
        $stmt->bindParam(':surname', $surname, SQLITE3_TEXT);
        $stmt->bindParam(':name', $name, SQLITE3_TEXT);
        $stmt->bindParam(':patronymic', $patronymic, SQLITE3_TEXT);
        $stmt->bindParam(':username', $username, SQLITE3_TEXT);
        $stmt->bindParam(':password', $password, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function addMark($student_id, $subject_id, $mark, $mdate)
    {
        $stmt = $this->conn->prepare("INSERT INTO marks (subject_id, mark, student_id, mdate) VALUES (:subject_id, :mark, :student_id, :mdate)");
        $stmt->bindParam(':subject_id', $student_id, SQLITE3_INTEGER);
        $stmt->bindParam(':mark', $mark, SQLITE3_INTEGER);
        $stmt->bindParam(':student_id', $student_id, SQLITE3_INTEGER);
        $stmt->bindParam(':mdate', $mdate, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function updateMark($markId, $newMark)
    {
        $stmt = $this->conn->prepare("UPDATE marks SET mark=:mark WHERE id=:markId");
        $stmt->bindParam(':mark', $newMark, SQLITE3_INTEGER);
        $stmt->bindParam(':markId', $markId, SQLITE3_INTEGER);
        $stmt->execute();
    }

    public function delMark($markId)
    {
        $stmt = $this->conn->prepare("DELETE FROM marks WHERE id=:markId;");
        $stmt->bindParam(':markId', $markId, SQLITE3_INTEGER);
        $stmt->execute();
    }

    public function getStudentsMarks($student_id)
    {
        $result = array();
        $stmt = $this->conn->prepare("SELECT * FROM marks WHERE student_id=:sid;");
        $stmt->bindParam(':sid', $student_id, SQLITE3_INTEGER);
        $pre_res = $stmt->execute();

        while ($tmp = $pre_res->fetchArray(SQLITE3_ASSOC)) {
            array_push($result, $tmp);
        }

        return array('values' => $result);
    }

    public function addSubject($name, $group_id, $host_id, $pass_type)
    {
        $stmt = $this->conn->prepare("INSERT INTO subjects (name, group_id, host_id, pass_type) VALUES (:name, :group_id, :host_id, :pass_type);");
        $stmt->bindParam(':name', $name, SQLITE3_TEXT);
        $stmt->bindParam(':group_id', $group_id, SQLITE3_INTEGER);
        $stmt->bindParam(':host_id', $host_id, SQLITE3_INTEGER);
        $stmt->bindParam(':pass_type', $pass_type, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function delSubject($subject_id)
    {
        $stmt = $this->conn->prepare("DELETE FROM subjects WHERE id=:subject_id;");
        $stmt->bindParam(':subject_id', $subject_id, SQLITE3_INTEGER);
        $stmt->execute();
    }

    public function getGroupSubjects($group_id)
    {
        $result = array();
        $stmt = $this->conn->prepare("SELECT * FROM subjects WHERE group_id=:group_id;");
        $stmt->bindParam(':group_id', $group_id, SQLITE3_INTEGER);
        $pre_res = $stmt->execute();

        while ($tmp = $pre_res->fetchArray(SQLITE3_ASSOC))
            array_push($result, $tmp);

        foreach ($result as &$val)
            $val['t_snp'] = $this->getTeacherSNP($val['host_id']);
        return array('values' => $result);
    }


    public function getTeacherSNP($teacher_id)
    {
        $stmt = $this->conn->prepare("SELECT surname || ' ' || name || ' ' || patronymic as snp FROM teachers WHERE id=:teacher_id;");
        $stmt->bindParam(':teacher_id', $teacher_id, SQLITE3_INTEGER);
        $result = $stmt->execute();
        return $result->fetchArray(SQLITE3_ASSOC)['snp'];
    }

    public function getStudentSNP($student_id)
    {
        $stmt = $this->conn->prepare("SELECT surname || ' ' || name || ' ' || patronymic as snp FROM students WHERE id=:student_id;");
        $stmt->bindParam(':student_id', $student_id, SQLITE3_INTEGER);
        $result = $stmt->execute();
        return $result->fetchArray(SQLITE3_ASSOC)['snp'];
    }

    public function getStudentAverage($student_id)
    {
        $stmt = $this->conn->prepare("SELECT avg(mark) as average FROM marks WHERE student_id=:student_id;");
        $stmt->bindParam(':student_id', $student_id, SQLITE3_INTEGER);
        $result = $stmt->execute();

        return $result->fetchArray(SQLITE3_ASSOC)['average'];
    }

    public function getGroupRating($group_id)
    {
        $result = [];
        $stms = $this->conn->prepare("SELECT
    (s.surname || ' ' || s.name ||  ' ' || s.patronymic) as snp,
    s.username as username,
    coalesce(AVG(m.mark), 0) as average
FROM students s
         LEFT JOIN marks m on m.student_id = s.id
WHERE s.group_id = :group_id
GROUP BY s.surname || ' ' || s.name || ' ' || s.patronymic, s.username
ORDER BY average DESC");

        $stms->bindParam(':group_id', $group_id, SQLITE3_INTEGER);
        $pre_res = $stms->execute();

        while ($tmp = $pre_res->fetchArray(SQLITE3_ASSOC))
            array_push($result, $tmp);

        return array('values' => $result);
    }

    public function getGlobalRating()
    {
        $result = [];
        $stms = $this->conn->prepare("SELECT 
       (s.surname || ' ' || s.name ||  ' ' || s.patronymic) as snp,
       s.username as username,
       AVG(m.mark) as average
FROM students s
JOIN marks m on m.student_id = s.id
GROUP BY s.surname || ' ' || s.name || ' ' || s.patronymic, s.username
ORDER BY average DESC
LIMIT 50");

        $pre_res = $stms->execute();

        while ($tmp = $pre_res->fetchArray(SQLITE3_ASSOC))
            array_push($result, $tmp);

        return array('values' => $result);
    }

    public function getCurrentSubjects($userId, $semester)
    {
        $result = [];
        $stms = $this->conn->prepare("
SELECT su.* FROM students s
JOIN groups g on s.group_id = g.id
JOIN subjects su on su.group_id = g.id
WHERE s.id = :userId and su.semester = :semester
ORDER BY su.name desc
");
        $stms->bindParam(':userId', $userId, SQLITE3_INTEGER);
        $stms->bindParam(':semester', $semester, SQLITE3_INTEGER);
        $pre_res = $stms->execute();

        while ($tmp = $pre_res->fetchArray(SQLITE3_ASSOC))
            array_push($result, $tmp);

        return array('values' => $result);
    }

    public function getTeacherBySubjectId($id)
    {
        $stmt = $this->conn->prepare("SELECT (t.surname || ' ' || t.name ||  ' ' || t.patronymic) as snp FROM subjects s join teachers t on s.host_id = t.id WHERE s.id = :sid;");
        $stmt->bindParam(':sid', $id, SQLITE3_INTEGER);
        $result = $stmt->execute();

        return $result->fetchArray(SQLITE3_ASSOC);
    }

    public function getSubjectById($id)
    {
        $stmt = $this->conn->prepare("SELECT * FROM subjects s WHERE s.id = :sid;");
        $stmt->bindParam(':sid', $id, SQLITE3_INTEGER);
        $result = $stmt->execute();

        return $result->fetchArray(SQLITE3_ASSOC);
    }

    public function getTasksForSubject($id)
    {
        $result = [];
        $stms = $this->conn->prepare("SELECT * FROM tasks WHERE subject_id=:id");

        $stms->bindParam(':id', $id, SQLITE3_INTEGER);
        $pre_res = $stms->execute();

        while ($tmp = $pre_res->fetchArray(SQLITE3_ASSOC))
            array_push($result, $tmp);

        return array('values' => $result);
    }

    public function updateSecret($newSecret, $id)
    {
        $stmt = $this->conn->prepare("UPDATE students SET passport = :newSecret WHERE id = :id;");
        $stmt->bindParam(':newSecret', $newSecret, SQLITE3_TEXT);
        $stmt->bindParam(':id', $id, SQLITE3_INTEGER);
        $stmt->execute();
    }

    public function getTaskById($task_id, $user_id)
    {
        $stmt = $this->conn->prepare("SELECT t.*, f.filename FROM tasks t
LEFT JOIN files f on f.task_id = t.id and f.student_id = :sid
WHERE t.id = :tid;");

        $stmt->bindParam(':tid', $task_id, SQLITE3_INTEGER);
        $stmt->bindParam(':sid', $user_id, SQLITE3_INTEGER);
        $result = $stmt->execute();

        return $result->fetchArray(SQLITE3_ASSOC);
    }

    public function updateFile($taskId, $student_id, $file, $filename)
    {
        $cd = date('Y-m-d H:i:s');
        $stmt = null;

        if (!is_null($this->getTaskById($taskId, $student_id)['filename'])) {
            $stmt = $this->conn->prepare("UPDATE files
SET
filename = :filename,
source = :source,
added_at = :added_at
WHERE task_id = :task_id and student_id = :student_id");

        } else {
            $stmt = $this->conn->prepare("INSERT INTO files (filename, source, added_at, task_id, student_id) values (:filename, :source, :added_at, :task_id, :student_id);");
        }
        $filename = uniqid() . $filename;
        $stmt->bindParam(':source', $file, SQLITE3_TEXT);
        $stmt->bindParam(':filename', $filename, SQLITE3_TEXT);
        $stmt->bindParam(':task_id', $taskId, SQLITE3_INTEGER);
        $stmt->bindParam(':student_id', $student_id, SQLITE3_INTEGER);
        $stmt->bindParam(':added_at', $cd, SQLITE3_TEXT);
        $stmt->execute();
    }

    public function loadFile($taskId, $student_id)
    {
        $stmt = $this->conn->prepare("SELECT f.filename as filename,
       f.source as source,
       f.added_at as added_at
       FROM tasks t
       JOIN files f on f.task_id = t.id and f.student_id = :sid 
       WHERE t.id = :tid;");
        $stmt->bindParam(':tid', $taskId, SQLITE3_INTEGER);
        $stmt->bindParam(':sid', $student_id, SQLITE3_INTEGER);
        $result = $stmt->execute();
        $data = $result->fetchArray(SQLITE3_ASSOC);
        if ($data)
            return array(base64_decode($data['source']), $data['filename'], $data['added_at']);
        return array('not found', null, null);
    }

    public function HasPermissionForTask($taskId, $userId)
    {
        $stmt = $this->conn->prepare("select 1 as result from tasks t
join subjects s on t.subject_id = s.id
join groups g on s.group_id = g.id
join students s2 on g.id = s2.group_id
where s2.id = :userId and t.id = :taskId");
        $stmt->bindParam(':userId', $userId, SQLITE3_INTEGER);
        $stmt->bindParam(':taskId', $taskId, SQLITE3_INTEGER);
        $result = $stmt->execute();

        return isset($result->fetchArray(SQLITE3_ASSOC)['result']);
    }

    public function initUser($group_id, $name, $surname, $patronymic, $user_id)
    {
        $stmt = $this->conn->prepare("UPDATE students SET surname = :surname, name = :name, patronymic = :patronymic, group_id = :group_id WHERE id = :user_id;");

        $stmt->bindParam(':surname', $surname, SQLITE3_TEXT);
        $stmt->bindParam(':name', $name, SQLITE3_TEXT);
        $stmt->bindParam(':patronymic', $patronymic, SQLITE3_TEXT);
        $stmt->bindParam(':group_id', $group_id, SQLITE3_INTEGER);
        $stmt->bindParam(':user_id', $user_id, SQLITE3_INTEGER);

        $stmt->execute();
    }

}