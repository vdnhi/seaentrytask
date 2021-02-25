import { Button, Card } from "@blueprintjs/core";

function FeedItem({ data }) {
  const startDate = new Date(data.start_date * 1000);
  const endDate = new Date(data.end_date * 1000);
  return (
    <Card>
      <div>Title: {data.title}</div>
      <div>Content: {data.content}</div>
      <div>Location: {data.location}</div>
      <div>Start date: {startDate.toLocaleDateString()} </div>
      <div>End date: {endDate.toLocaleDateString()}</div>
      <Button>See more</Button>
    </Card>
  );
}

export default FeedItem;
