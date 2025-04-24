import React, {Component} from 'react';
import { Link } from "react-router-dom";
import { 
    Media, 
    Button, 
    Label, 
    Col, 
    Row, 
	Breadcrumb, 
	BreadcrumbItem 
} from 'reactstrap';
import { Loading } from './LoadingComponent';
import Slider from './SliderComponent';
import { Control, Form, Errors } from 'react-redux-form';

import { RatePostWithStars, StarRating }  from './StarRatingComponent';

const required = (val) => val && val.length;
//const maxLength = (len) => (val) => !(val) || (val.length <= len);
const minLength = (len) => (val) => val && (val.length >= len);

/**
 * Comments form
 */
class Comment extends Component {

    constructor(props){
        super(props);


        this.handleSubmit = this.handleSubmit.bind(this);
    }

    /**
     * 
     * Send parameters to do the post request and clear fields in the view
     */
    handleSubmit(values){
        //console.log("Current State is: "+ JSON.stringify(this.props.postId + ", " +values))
        //alert("Current State is: "+ JSON.stringify(this.props.postId + ", " +values));
        this.props.postComment(this.props.postId, values.comment)
        this.props.resetCommentForm();
    }

    /**
     * Render form with their respective validations
     */
    render(){

        return(
            <div className="container">
                <div className="row row-content">
                    <div className="col-12">
                        <h4>Make a comment about this post</h4>
                    </div>
                    <div className="col-12 col-md-9">
                        <Form model="comment" onSubmit={(values) => this.handleSubmit(values)}>
                            <Row className="form-group">
                                <Label htmlFor="comment" md={2}>Comment</Label>
                                <Col md={10}>
                                    <Control.textarea model=".comment" id="comment" name="comment"
                                        rows="6"
                                        className="form-control"
                                        validators={{
                                            required, minLength: minLength(3)
                                        }} 
                                    />
                                    
                                    <Errors 
                                        className="text-danger"
                                        model=".comment" 
                                        show="touched" 
                                        messages={{
                                            required: 'Required',
                                            minLength: ' Must be greater than 2 characters'
                                        }}
                                        />
                                </Col>
                            </Row>
                            <Row className="form-group">
                                <Col md={{size:10, offset: 2}}>
                                    <Button type="submit" color="primary">
                                    Send comment
                                    </Button>
                                </Col>
                            </Row>
                        </Form>
                    </div>
                </div>
            </div>
        );
    }

}


/**
 * Render comments
 */
function RenderComments({comments, profile_images}){
    
    const profile_images2 = profile_images.profile_images;
    return (
        <div className="container">
          <div className="row">
            <Media list>
                    {comments.map((comment) => {
                        const profile_image = profile_images2.filter((profile_image) => profile_image.user === comment.author);

                        return (
                            <div key={comment.id} className="col-12 mt-5">
                                <Media tag="li">
                                    <Media left middle>
                                        <Media className="commentimg" object src={profile_image[0].profile_image} alt={comment.nickname} />
                                    </Media>
                                    <Media body className="ml-5">
                                        <h6>{comment.username}</h6>
                                        <p>{comment.content}</p>
                                        <p>{new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day:'2-digit', hour: 'numeric', minute: 'numeric', second: 'numeric'}).format(new Date(Date.parse(comment.datetime)))}</p>
                                    </Media>
                                </Media>
                            </div>
                        );
                    })}
            </Media>
          </div>
        </div>
    );            
}

/**
 * Show status if the page is Loading shows spinner else shows error or the page content
 */
const PostContent = (props) => {
    
	if (props.postisLoading || props.profile_imagesisLoading) {
		
        return(
            <Loading />
        );
    }
    else if (props.posterrMess) {
        return(
            <h4>{props.posterrMess}</h4>
        );
    }
    else if (props.profile_imageserrMess) {
        return(
            <h4>{props.profile_imageserrMess}</h4>
        );
    }
	else{ 
		console.log(JSON.stringify(props  ) +   ' postcontent');
		return(


			<div className="container">
                <br />
                <div className="row">
                    <div className="col">
                        <Breadcrumb>
                            <BreadcrumbItem><Link to='/home'>Home</Link></BreadcrumbItem>
                            <BreadcrumbItem active>{props.post.slug}</BreadcrumbItem>
                        </Breadcrumb>
                    </div>
                </div>			
				<div className="row row-content">
					<div className="col-12">
						<h2 align="center">{props.post.title}</h2>
						<hr />
						<img top width="100%" src={props.post.image_post} alt={props.post.title} />
					</div>                
				</div>
				<div className="row row-content">
					<div className="col-12">
						
                        <h5>Created on:</h5>
						<p>{new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day:'2-digit', hour: 'numeric', minute: 'numeric', second: 'numeric'}).format(new Date(Date.parse(props.post.created_on)))}</p>
                        
                        <h5>Genre:</h5>
						{/**
						 * Source: https://stackoverflow.com/a/50287386/9655579
						 */}
						<p>{props.post.genres.map(e => e.name).join(' | ')}</p>
						
                        <h5>Rating:</h5>
                        {props.post.avg_rating ?
						    <StarRating totalStars={5} starsSelected={props.post.avg_rating} />
						:
                            <p>This post is not voted</p>
                        }

                        <h5>Sinopsis:</h5>
						<p className="textPost">{props.post.description}</p>
						
						<h5>Description:</h5>
						<p className="textPost">{props.post.content}</p>
					</div>
				</div>
				<div className="row">
					<div className="col">
						<Slider dataposts={props.post.imageps} />
					</div>
				</div>
				<div className="row">
					<div className="col">
                        <br />
						<h5>Updated on:</h5>
						<p>{new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day:'2-digit', hour: 'numeric', minute: 'numeric', second: 'numeric'}).format(new Date(Date.parse(props.post.updated_on)))}</p>
					</div>
				</div>
				<div className="row">
                    <div className="col">
                        <br />
                        <h5>Rate this post</h5>
                        {props.isAbleToMakeComments ?
                            <RatePostWithStars totalStars={5} postId={props.post.id} ratePost={props.ratePost}  />
                        :
                            <h7>Only authenticated users are able to rate this post</h7>
                        }
                    </div>
				</div>
                <div className="row row-content">
                    <div className="col-12">
                        <h2>Comments</h2>
                    </div>
                    <div className="col-12">
                        {props.isAbleToMakeComments ?
                            <Comment postId={props.post.id} resetCommentForm={props.resetCommentForm} postComment={props.postComment} />
                            : 
                            <h7>Only authenticated users are able to make comments on this post</h7>
                        }
                        
                    </div>
                    <div className="col-12">
                        <RenderComments comments={props.comments.filter((comment) => comment.post === props.post.id)} profile_images={props.profile_images} />
                    </div>
                </div>				
			</div>

        );
	}
}



export default PostContent;