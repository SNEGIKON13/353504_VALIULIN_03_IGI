import React, { Component } from 'react';

import { 
	Button,
	Form
} from 'reactstrap';

const Star = ({ selected=false, onClick=f=>f }) => (
    <div className={ (selected) ? "star selected" : "star" } onClick={onClick}>
    </div>
)

export class RatePostWithStars extends Component {
    constructor(props) {
        super(props)
        this.state = { starsSelected: 1 }
        this.change = this.change.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this);
    }


    change(starsSelected) {
        this.setState({ starsSelected: starsSelected })
    }

    /**
     * 
     * Send parameters to do the post request
     */
     handleSubmit(){
        //console.log("Current State is: "+ JSON.stringify(this.props.postId + ", " +values))
        //alert("Current State is: "+ JSON.stringify(this.props.postId + ", " +this.state.starsSelected));
        this.props.ratePost(this.props.postId, this.state.starsSelected)
    }
    
    render() {
        const { totalStars } = this.props
        const { starsSelected } = this.state

        return(
            <div className="star-rating">
                {[...Array(totalStars)].map((n,i) => 
                    <Star 
                        key={i}
                        selected={i<starsSelected}
                        onClick={() => this.change(i+1)}
                    />
                 )}
                <p>{starsSelected} of {totalStars} stars</p>
                <Form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="submit" color="secondary">Send rating</Button>
                </Form>
            </div>
        )
    }
}

export class StarRating extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        const { totalStars } = this.props.totalStars
        const { starsSelected } = this.props.starsSelected

        return(
            <div className="star-rating">
                {[...Array(this.props.totalStars)].map((n,i) => 
                    <Star 
                        key={i}
                        selected={i<this.props.starsSelected}
                    />
                 )}
                <p>{this.props.starsSelected} of {this.props.totalStars} stars</p>
            </div>
        )
    }
}
