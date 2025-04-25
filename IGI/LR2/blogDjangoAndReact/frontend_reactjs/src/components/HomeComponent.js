import React from 'react';
import { Link } from "react-router-dom";
import { Loading } from './LoadingComponent';
import { 
	Card, 
	CardImg, 
	CardText, 
	CardBody, 
	CardTitle, 
	Nav, 
	NavItem, 
	NavLink, 
	Breadcrumb, 
	BreadcrumbItem,
	Button
	
} from 'reactstrap';
import Slider from './SliderComponent';
import { FadeTransform } from 'react-animation-components';
import { RatePostWithStars, StarRating }  from './StarRatingComponent';

/**
 * Show status if the page is Loading shows spinner else shows error or the page content
 */
const Home = (props) => {
	
	
	if (props.genres.isLoading) {
		
        return(
            <Loading />
        );
    }
    else if (props.genres.errMess) {
        return(
            <h4>{props.genres.errMess}</h4>
        );
    }
	else{ 
		/**
		 * Iterate over object that is in the store
		 */
		//console.log(JSON.stringify(props.featured_posts  ) +   ' postcontent');
		return(
			<>
			
				<Slider dataposts={props.featuredposts.featuredposts} />
				<br />
				<div className="container">

					{/*<h2 align="center">Categories</h2>*/}
					<div className="row">
						<div className="col">
							<Breadcrumb>
								<BreadcrumbItem active>Home</BreadcrumbItem>
							</Breadcrumb>
						</div>
					</div>
					<div className="row row-content">
						
						<div className="col-12 col-sm-4 order-sm-first col-md-2 sidebarGenres">
							
							
							<div className="row">
								<Nav vertical navbar>
									<h5 align="center">Categories</h5>
									{props.genres.genres.map((field, i) => { 
										return(
											<div className="col">
											<NavItem>
											
												<NavLink className="linkGenre" tag={Link} to={`/genre/${field.slug}`}>{field.name}</NavLink>
											</NavItem>
											</div>
										);
										
									}) }
								</Nav>
								{/*<ButtonGroup vertical size="lg" className="mb-2">
									<Button disabled><h4>Categories</h4></Button>
									{/*props.genres.genres.map((field, i) => { 
										return(
											<Link to={`/genre/${field.slug}`} ><Button>{field.name}</Button></Link>
										);
										
									}) */}
								{/*</ButtonGroup>*/}
							</div>
							
						</div>
						<div className="col col-sm order-sm-last col-md">
							<h5 align="center">Latest posts</h5>
							
							<div className="row row-content">
							{
								props.posts.posts.map((field, i) => { 
									return(
									
										<div key={field._id} className="col-12 col-md-4 m-20 postCard">
											<FadeTransform in 
												transformProps={{
													exitTransform: 'scale(0.5) translateY(-50%)'
												}}>
													<Card>
														<Link to={`/post/${field.slug}`} >
															<CardImg className="postImage" src={field.image_post} alt={field.title} />
														</Link>
														<CardBody>
															<CardTitle className="postCardTitle">{field.title}</CardTitle>
															<CardText className="postCardDescription">
																{(field.description).substr(0,150)}...
															</CardText>
															<div align="center">
																<Link to={`/post/${field.slug}`} >
																	<Button color="secondary">Read more</Button>
																</Link>
															</div>
														</CardBody>
														
													</Card>		
													{/*<RatePostWithStars totalStars={5} />*/}
													{/*<StarRating totalStars={5} starsSelected={3} />*/}
											</FadeTransform>
										</div>		
																		
									);
									
								}) 
							}
							</div>
						</div>
					</div>			
				</div>
			</>
        );
	}
}



export default Home;