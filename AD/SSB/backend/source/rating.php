<?php


class Rating
{
    private $db;
    private $id;

    public function __construct()
    {
        $this->db = new DataBase();
        $this->id = $_SESSION['id'];
    }

    public function getGroupRating()
    {
        $user = $this->db->getStudent($this->id, null);
        return generate_true_callback($this->db->getGroupRating($user['group_id']));
    }

    public function getGlobalRating()
    {

        return generate_true_callback($this->db->getGlobalRating($this->id));
    }

}