import { Button } from "@blueprintjs/core";
import axios from "axios";
import { useEffect, useState } from "react";
import AddEventForm from "../components/AddEventForm";
import FeedItem from "../components/FeedItem";

function EventFeed() {
  const [feedItems, setFeedItems] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    const userId = window.sessionStorage.getItem('userId');
    const token = window.sessionStorage.getItem('token');
    axios
      .get(`/event/?offset=5&user_id=${userId}&token=${token}`)
      .then((response) => setFeedItems(response.data))
      .catch((error) => console.log(error));
  }, [dialogOpen]);

  return (
    <div>
      <div>Left Tab</div>
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
    </div>
  );
}

export default EventFeed;
