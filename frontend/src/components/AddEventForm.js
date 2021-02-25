import {
  Button,
  Dialog,
  Classes,
  Intent,
  FormGroup,
  InputGroup,
  TextArea,
  MenuItem,
  FileInput,
} from "@blueprintjs/core";
import { DateRangeInput } from "@blueprintjs/datetime";
import { MultiSelect } from "@blueprintjs/select";
import axios from "axios";

import { useEffect, useState } from "react";
import { AppToaster } from "./Toaster";

function AddEventForm({ isOpen, toggleOpen }) {
  const [isAddingEvent, setIsAddingEvent] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [location, setLocation] = useState("");
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [channels, setChannels] = useState([]);
  const [selectedChannels, setSelectedChannels] = useState([]);
  const [images, setImages] = useState([]);

  useEffect(() => {
    axios
      .get("event/channel/")
      .then((response) => setChannels(response.data))
      .catch((error) => console.log(error));
  }, []);

  const clearInput = () => {
    setTitle("");
    setContent("");
    setLocation("");
    setStartDate(null);
    setEndDate(null);
    setChannels([]);
    setSelectedChannels([]);
    setImages([]);
  };

  const handleAddingEvent = () => {
    setIsAddingEvent(true);
    const userId = parseInt(window.sessionStorage.getItem("userId"));
    const token = window.sessionStorage.getItem("token");

    axios
      .post("/event/", {
        title: title,
        content: content,
        start_date: Math.round(startDate?.getTime() / 1000),
        end_date: Math.round(endDate?.getTime() / 1000),
        channels: selectedChannels,
        location: location,
        create_uid: userId,
        token: token,
      })
      .then((response) => {
        const eventId = response.data["id"];
        const formdata = new FormData();

        formdata.append("image", images[0]);
        formdata.append("user_id", userId);
        formdata.append("token", token);

        axios
          .post(`/event/${eventId}/uploadImage/`, formdata, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            console.log(response);
            toggleOpen(false);
            clearInput();
          })
          .catch((error) => console.log(error));
      })
      .catch((error) => {
        console.log(error);
        AppToaster.show({
          message: "Add event failed!",
          intent: "danger",
          timeout: 1000,
        });
      });
    setIsAddingEvent(false);
  };

  const channelSelectItemRenderer = (item) => {
    return (
      <MenuItem label={item.name} onClick={() => handleSelectChannel(item)} />
    );
  };

  const handleSelectChannel = (item) => {
    setSelectedChannels([...selectedChannels, item]);
    setChannels([...channels.filter((oldItem) => oldItem !== item)]);
  };

  const removeSelectItem = (item) => {
    setChannels([...channels, item]);
    setSelectedChannels([
      ...selectedChannels.filter((sItem) => sItem !== item),
    ]);
  };

  const selectedChannelsRenderer = (item) => {
    return <div>{item.name}</div>;
  };

  const handleUploadImage = (event) => {
    let new_images = [...images];
    Array.from(event.target.files).forEach((image) => new_images.push(image));
    setImages(new_images);
  };

  return (
    <Dialog
      icon="info-sign"
      title="Add new event"
      isOpen={isOpen}
      onClose={() => {
        toggleOpen(false);
        clearInput();
      }}
    >
      <div className={Classes.DIALOG_BODY}>
        <FormGroup
          label="Title"
          labelFor="text-input-title"
          labelInfo="(required)"
        >
          <InputGroup
            id="text-input-title"
            placeholder="Event title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required={true}
          />
        </FormGroup>
        <FormGroup
          label="Content"
          labelFor="text-input-content"
          labelInfo="(required)"
        >
          <TextArea
            id="text-input-content"
            placeholder="Content..."
            value={content}
            style={{ width: "100%" }}
            onChange={(e) => setContent(e.target.value)}
            type="textarea"
            required={true}
          />
        </FormGroup>
        <FormGroup
          label="Location"
          labelFor="text-input-location"
          labelInfo="(required)"
        >
          <TextArea
            id="text-input-location"
            placeholder="Location..."
            value={location}
            style={{ width: "100%" }}
            onChange={(e) => setLocation(e.target.value)}
            type="textarea"
            required={true}
          />
        </FormGroup>

        <FormGroup
          label="Event date"
          labelFor="date-input-event-date"
          labelInfo="(required)"
        >
          <DateRangeInput
            formatDate={(date) => date.toLocaleString()}
            onChange={(range) => {
              setStartDate(range[0]);
              setEndDate(range[1]);
            }}
            parseDate={(str) => new Date(str)}
            value={[startDate, endDate]}
            highlightCurrentDay={true}
          />
        </FormGroup>
        <FormGroup label="Channels" labelFor="multi-input-channel">
          <MultiSelect
            fill={true}
            tagInputProps={{ placeholder: "Search for channel" }}
            itemRenderer={channelSelectItemRenderer}
            tagRenderer={selectedChannelsRenderer}
            onRemove={removeSelectItem}
            items={channels}
            selectedItems={selectedChannels}
            onItemSelect={handleSelectChannel}
          />
        </FormGroup>
        <FormGroup label="Images" labelFor="image-upload">
          <FileInput
            fill={true}
            id="image-upload"
            text={"Choose image..."}
            onInputChange={handleUploadImage}
            inputProps={{ accept: "image/png, image/jpeg, image/jpg" }}
          />
          <div>
            {images.map((image, index) => (
              <div key={index}>{image.name}</div>
            ))}
          </div>
        </FormGroup>
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <div className={Classes.DIALOG_FOOTER_ACTIONS}>
          <Button
            text="Add"
            intent={Intent.PRIMARY}
            onClick={handleAddingEvent}
            loading={isAddingEvent}
            large={true}
          />
        </div>
      </div>
    </Dialog>
  );
}

export default AddEventForm;
