import React from 'react';
import { Link } from "react-router-dom";
import { Loading } from './LoadingComponent';
import { 
	Card, 
	CardImg, 
	CardText, 
	CardBody, 
	CardTitle,
	Breadcrumb, 
	BreadcrumbItem,
	Button
} from 'reactstrap';

/**
 * Show status if the page is Loading shows spinner else shows error or the page content
 */
const GenreContent = (props) => {
	
	
	if (props.isLoading) {
		
        return(
            <Loading />
        );
    }
    else if (props.errMess) {
        return(
            <h4>{props.errMess}</h4>
        );
    }
	else{ 
		/**
		 * Iterate over object that is in the store
		 */
		return(
			<div className="container">
				<br />
				<div className="row">
					<div className="col">
						<Breadcrumb>
							<BreadcrumbItem><Link to='/home'>Home</Link></BreadcrumbItem>
							<BreadcrumbItem active>{props.genre.slug}</BreadcrumbItem>
						</Breadcrumb>
					</div>
				</div>				
				<h2 align="center">Posts</h2>
					
				<div className="row row-content">
						
					{props.genre.postsgen.map((field, i) => { 
						
						return(
						<div key={field._id} className="col-12 col-md-4 m-20 postCard">
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
						</div>				
				
						);
						
					}) }


				</div>

							
			</div>
        );
	}
}



export default GenreContent;