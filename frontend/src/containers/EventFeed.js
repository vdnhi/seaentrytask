import { Button } from "@blueprintjs/core";
import axios from "axios";
import { useEffect, useState } from "react";
import AddEventForm from "../components/AddEventForm";
import FeedItem from "../components/FeedItem";

function EventFeed() {
  const [feedItems, setFeedItems] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    const userId = window.sessionStorage.getItem("userId");
    const token = window.sessionStorage.getItem("token");
    axios
      .get(`/event/?offset=5&user_id=${userId}&token=${token}`)
      .then((response) => setFeedItems(response.data))
      .catch((error) => console.log(error));
  }, [dialogOpen]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        flexWrap: "wrap",
        width: "100%",
        justifyContent: 'space-between'
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          flexBasis: "100%",
          flex: 2,
          margin: '20px 0px 20px 0px'
        }}
      >
        <Button
          text="Create new event"
          icon="add"
          onClick={() => setDialogOpen(true)}
        />
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          flexBasis: "100%",
          flex: 8,
        }}
      >
        {feedItems.map((item, index) => (
          <FeedItem data={item} key={index} />
        ))}
        <AddEventForm isOpen={dialogOpen} toggleOpen={setDialogOpen} />
      </div>
    </div>
  );
}

export default EventFeed;
