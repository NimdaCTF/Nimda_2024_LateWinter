<?php

class User
{
    private $db;
    private $id;

    public function __construct()
    {
        $this->db = new DataBase();
        $this->id = $_SESSION['id'];
    }

    public function updateSNP($surname, $name, $patronymic)
    {
        preg_match('/^[A-Za-zА-Яа-я\-]{2,35}$/', $surname, $sm);
        preg_match('/^[A-Za-zА-Яа-я\-]{2,35}$/', $name, $nm);

        if (count($sm) < 1 || count($nm) < 1)
            return generate_error_callback('Invalid snp credentials');

        $user = $this->db->getStudent($_SESSION['id']);
        if ($user['surname'] === '' && $user['name'] === '' && $user['patronymic'] === '') {
            $this->db->updateSNP($surname, $name, $patronymic, $_SESSION['id']);
            return generate_true_callback();
        }
        return generate_error_callback('You can\'t change SNP credentials.');
    }

    public function getUser()
    {
        $result = $this->db->getStudent($this->id, null);
        unset($result['password']);

        return generate_true_callback($result);
    }

    public function getSubjects()
    {
        $group_id = $this->db->getStudent($this->id, null)['group_id'];
        return generate_true_callback($this->db->getGroupSubjects($group_id));
    }

    public function getMarks()
    {
        return generate_true_callback($this->db->getStudentsMarks($this->id));
    }

    public function setSecret($newSecret)
    {
        $this->db->updateSecret($newSecret, $this->id);
        return generate_true_callback();
    }

    public function uploadFile($taskId, $file, $filename)
    {
        if (!$this->db->HasPermissionForTask($taskId, $this->id)) {
            return generate_error_callback('F0rb1dd3n, buddy.', 403);
        }
        $this->db->updateFile($taskId, $this->id, $file, $filename);
        return generate_true_callback();
    }

    public function init($group_id, $snp)
    {
        $snp = explode(' ', $snp);
        if (count($snp) < 2 || count($snp) > 3) {
            return generate_error_callback('Invalid snp', 400);
        }

        if (empty($snp[3])) {
            $snp[3] = '';
        }
        $this->db->initUser($group_id, $snp[1], $snp[0], $snp[3], $this->id);

        return generate_true_callback();
    }
}