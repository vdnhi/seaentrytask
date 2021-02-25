import { Button } from "@blueprintjs/core";
import axios from "axios";
import { useEffect, useState } from "react";
import AddEventForm from "../components/AddEventForm";
import FeedItem from "../components/FeedItem";

function EventFeed() {
  const [feedItems, setFeedItems] = useState([{}]);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    axios
      .get("/event/?offset=5")
      .then((response) => setFeedItems(response.data))
      .catch((error) => console.log(error));
  }, []);

  return (
    <div>
      <Button
        text="Create new event"
        icon="add"
        onClick={() => setDialogOpen(true)}
      />
      {feedItems.map((item, index) => (
        <FeedItem data={item} key={index} />
      ))}
      <AddEventForm isOpen={dialogOpen} toggleOpen={setDialogOpen} />
    </div>
  );
}

export default EventFeed;
