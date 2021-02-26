import { Button, Card, Position } from "@blueprintjs/core";
import { FLEX_EXPANDER } from "@blueprintjs/core/lib/esm/common/classes";
import axios from "axios";
import { useState, useEffect } from "react";

function FeedItem({ data }) {
  const [countLike, setCountLike] = useState(0);
  const [isLiked, setIsLiked] = useState(false);
  const startDate = new Date(data.start_date * 1000);
  const endDate = new Date(data.end_date * 1000);

  const userId = parseInt(window.sessionStorage.getItem("userId"));
  const token = window.sessionStorage.getItem("token");

  useEffect(() => {
    axios
      .get(`/event/${data.id}/like/`, {
        user_id: userId,
      })
      .then((response) => {
        const usersLiked = response.data;
        const liked =
          usersLiked.filter((item) => item.id === userId).length > 0;
        if (liked) {
          setIsLiked(true);
        }
        setCountLike(usersLiked.length);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [isLiked]);

  const handleClickLikeButton = () => {
    if (!isLiked) {
      axios
        .post(`/event/${data.id}/like/`, {
          user_id: userId,
          token: token,
        })
        .then((response) => {
          setCountLike(countLike + 1);
          setIsLiked(true);
        })
        .catch((error) => {
          console.log(error);
        });
    } else {
      axios
        .delete(`/event/${data.id}/like/?user_id=${userId}&token=${token}`)
        .then((response) => {
          setIsLiked(false);
        })
        .catch((error) => console.log(error));
    }
  };

  return (
    <Card>
      <div>Title: {data.title}</div>
      <div>Content: {data.content}</div>
      <div>Location: {data.location}</div>
      <div>Start date: {startDate.toLocaleDateString()} </div>
      <div>End date: {endDate.toLocaleDateString()}</div>
      <div>Number of like: {countLike}</div>
      <div style={{display: 'flex', justifyContent: 'space-around'}}>
      {data.image_urls.map((image_url) => (
        <img src={image_url} style={{ maxWidth: 200, maxHeight: 200 }}></img>
      ))}

      </div>
      <Button
        text={isLiked ? "Remove like" : "Like"}
        onClick={handleClickLikeButton}
      />
    </Card>
  );
}

export default FeedItem;
