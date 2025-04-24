/**
 * Source official documentation: https://reactstrap.github.io/components/carousel/
 */

import React, { useState } from 'react';
import {
  Carousel,
  CarouselItem,
  CarouselControl,
  CarouselIndicators,
  CarouselCaption
} from 'reactstrap';

import { Link } from "react-router-dom";

/**
 * Arrow function Image
 * if item has a slug it returns an image with a link to the post
 * else it just returns the image (Slider of images within a post)
 * The img width is fixed in App.css file
 */
const Image = (props) => {
  if (props.item.slug) {
    return (
      <Link to={`/post/${props.item.slug}`} >
        <img src={props.item.image_post} alt={props.item.title} />
      </Link>
    );
  }else{
    return (
      <img src={props.item.image_post} alt={props.item.title} />
    );
  }
}

/**
 * Arrow function uses images, title from props (featured posts)
 * for retrieving featured posts using the slider
 */
const Slider = (props) => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [animating, setAnimating] = useState(false);

  const next = () => {
    if (animating) return;
    const nextIndex = activeIndex === props.dataposts.length - 1 ? 0 : activeIndex + 1;
    setActiveIndex(nextIndex);
  }

  const previous = () => {
    if (animating) return;
    const nextIndex = activeIndex === 0 ? props.dataposts.length - 1 : activeIndex - 1;
    setActiveIndex(nextIndex);
  }

  const goToIndex = (newIndex) => {
    if (animating) return;
    setActiveIndex(newIndex);
  }

  const slides = props.dataposts.map((item) => {
    return (
      <CarouselItem
        onExiting={() => setAnimating(true)}
        onExited={() => setAnimating(false)}
        key={item.id}
      >
        <Image item={item} />
        <CarouselCaption captionText={item.description} captionHeader={item.title} />
      </CarouselItem>
    );
  });

  return (
    <Carousel
      activeIndex={activeIndex}
      next={next}
      previous={previous}
    >
      <CarouselIndicators items={props.dataposts} activeIndex={activeIndex} onClickHandler={goToIndex} />
      {slides}
      <CarouselControl direction="prev" directionText="Previous" onClickHandler={previous} />
      <CarouselControl direction="next" directionText="Next" onClickHandler={next} />
    </Carousel>
  );
}

export default Slider;