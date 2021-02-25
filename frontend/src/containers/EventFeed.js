import { useEffect, useState } from "react";
import FeedItem from "../components/FeedItem";

function EventFeed() {
  const [feedItems, setFeedItems] = useState([{}]);

  useEffect(() => {
  }, []);

  return (
    <div>
      {feedItems.map((item) => (
        <FeedItem data={item} />
      ))}
    </div>
  );
}

export default EventFeed;
