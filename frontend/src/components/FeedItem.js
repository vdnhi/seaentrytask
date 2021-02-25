import { Button, Card } from "@blueprintjs/core";

function FeedItem({ data }) {
  return (
    <Card>
      <div>{data.title}</div>
      <div>{data.content}</div>
      <div>{data.location}</div>
      <Button>See more</Button>
    </Card>
  );
}

export default FeedItem;
