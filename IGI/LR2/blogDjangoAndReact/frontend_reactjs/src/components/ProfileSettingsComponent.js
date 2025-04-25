import React, { Component } from 'react';
import { 
	Button, 
	Form, 
	FormGroup, 
	Input, 
    Label, 
} from 'reactstrap';


import { withRouter } from 'react-router-dom';
import { connect } from 'react-redux';

/* Set data gotten from Django API with redux to the Cpmponent's props */
/*const mapStateToProps = state => {
    return{
      user_data: state.user_data,
    }
}*/

/* Set functions from ActionCreators redux to the Cpmponent's props and dispatch */
/*const mapDispatchToProps = (dispatch) => ({
    fetchUserData: () => { dispatch(fetchUserData())},
});*/

/**
 * User profile form
 */

class ProfileSettingsComponent extends Component {

    constructor(props){
        super(props);

        this.handleRegister = this.handleRegister.bind(this);
    }

  //Execute this before render
  /*componentDidMount() {
    this.props.fetchUserData();
  }*/
    /**
     * 
     * Send parameters to do the post request and clear fields in the view
     */

    handleRegister(event) {
        //this.toggleModal();
        this.props.updateUser({
            email: this.email.value, 
            first_name: this.first_name.value, 
            last_name: this.last_name.value, 
        });
        
        event.preventDefault();

    }    
    

    /**
     * Render form with their respective validations
     */
    render(){
        
    console.log("Props2");
    console.log(this.props.user_data.user_data.first_name);
        return(
            <div className="container">
                <div className="row row-content">
                    <div className="col-12">
                        <h4>Profile settings</h4>
                    </div>
                    <div className="col-12 col-md-9">

                        <Form onSubmit={this.handleRegister}>
                            <FormGroup>
                                <Label htmlFor="first_name">First name</Label>
                                <Input type="text" id="first_name" name="first_name" defaultValue={this.props.user_data.user_data.first_name}
                                    innerRef={(input) => this.first_name = input} />
                            </FormGroup>
                            <FormGroup>
                                <Label htmlFor="last_name">Last name</Label>
                                <Input type="text" id="last_name" name="last_name" defaultValue={this.props.user_data.user_data.last_name}
                                    innerRef={(input) => this.last_name = input} />
                            </FormGroup>
                            <FormGroup>
                                <Label htmlFor="email">Email address</Label>
                                <Input type="email" id="email" name="email" defaultValue={this.props.user_data.user_data.email}
                                    innerRef={(input) => this.email = input} />
                            </FormGroup>
                            <FormGroup check>
                                <Label check>
                                    <Input type="checkbox" name="remember"
                                    innerRef={(input) => this.remember = input}  />
                                    Remember me
                                </Label>
                            </FormGroup>
                            <Button type="submit" value="submit" color="secondary">Edit</Button>
                        </Form>
                    </div>
                </div>
            </div>
        );
    }

}

//export default ProfileSettingsComponent;


export default ProfileSettingsComponent;