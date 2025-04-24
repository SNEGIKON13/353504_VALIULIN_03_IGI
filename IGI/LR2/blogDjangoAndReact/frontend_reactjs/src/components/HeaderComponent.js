import React, { Component, useState } from 'react';
import { 
	Navbar, 
	NavbarBrand, 
	Nav, 
	NavbarToggler, 
	Collapse, 
	NavItem, 
	Button, 
	Modal, 
	ModalHeader, 
	ModalBody,
	Form, 
	FormGroup, 
	Input, 
    Label, 
    TabContent, 
    TabPane, 
    Dropdown, 
    DropdownToggle, 
    DropdownMenu, 
    DropdownItem 
} from 'reactstrap';
import { NavLink } from 'react-router-dom';
import classnames from 'classnames';

const DropdownMenuComponent = (props) => {
    const [dropdownOpen, setDropdownOpen] = useState(false);
  
    const toggle = () => setDropdownOpen(prevState => !prevState);

    return (
      <Dropdown isOpen={dropdownOpen} toggle={toggle}>
        <DropdownToggle caret>
            <img src={props.user_data.user_data.profile_image} height="30" width="41" alt="My blog" />
        </DropdownToggle>
        <DropdownMenu right>
          <DropdownItem header>{props.auth.user.username}</DropdownItem>
          <DropdownItem>
              
            <NavLink className="linkGenre" to="/profile-settings">
                Profile settings
            </NavLink>
              
          </DropdownItem>
          <DropdownItem text>Dropdown Item Text</DropdownItem>
          <DropdownItem disabled>Action (disabled)</DropdownItem>
          <DropdownItem divider />
          {/*<DropdownItem>Foo Action</DropdownItem>*/}
          <DropdownItem>
            <a onClick={props.handleLogout} id="loginButton" role="button">
                <span className="fa fa-sign-out fa-lg"></span> Logout
            </a>
            {props.auth.isFetching ?
                <span className="fa fa-spinner fa-pulse fa-fw"></span>
                : null
            }
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>
    );
  }

class Header extends Component{
	constructor(props) {
	    super(props);

	    this.toggleNav = this.toggleNav.bind(this);
        this.toggleModal = this.toggleModal.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
        this.handleLogout = this.handleLogout.bind(this);
        this.handleRegister = this.handleRegister.bind(this);

        this.toggleTab = this.toggleTab.bind(this);

	    this.state = {
		  isNavOpen: false,
          isModalOpen: false,
          activeTab: '1',
          profile_image: null
	    };
	}

	toggleNav() {
	    this.setState({
	      isNavOpen: !this.state.isNavOpen
	    });
    }

    //Open modal
    toggleModal() {
        this.setState({
            isModalOpen: !this.state.isModalOpen
        });
    }

    toggleTab(tab) {
        if (this.state.activeTab !== tab) {
          this.setState({ activeTab: tab });
        }
    }
    //Call loginUser functions
    handleLogin(event) {
        this.toggleModal();
        this.props.loginUser({username: this.username.value, password: this.password.value});
        event.preventDefault();

    }

    handleImageChange = (e) => {
        this.setState({
            profile_image: e.target.files[0]
        })
    };

    handleLogout() {
        this.props.logoutUser();
    }

    handleRegister(event) {
        this.toggleModal();
        this.props.registerUser({
            username: this.username.value, 
            email: this.email.value, 
            first_name: this.first_name.value, 
            last_name: this.last_name.value, 
            password: this.password.value, 
            profile_image: this.state.profile_image
        });
        /*
        this.props.registerUser(
            this.username.value, 
            this.email.value, 
            this.first_name.value, 
            this.last_name.value, 
            this.password.value, 
            this.state.profile_image
        );*/
        event.preventDefault();

    }    
    
	render(){
		return(
			<>
				<Navbar dark expand="md">
					<div className="container">
						<NavbarToggler onClick={this.toggleNav} />
						<NavbarBrand className="mr-auto">
							<img src="/assets/images/logo1.jpg" height="30" width="41" alt="My blog" />
						</NavbarBrand>
						<Collapse isOpen={this.state.isNavOpen} navbar>
							<Nav navbar>
								<NavItem>
									<NavLink className="nav-link" to="/home">
										<span className="fa fa-home fa-lg"></span> Home  
									</NavLink>
								</NavItem>
							</Nav>
                            <Nav className="ml-auto navbar-dark" navbar>
                                <NavItem>
                                    { !this.props.auth.isAuthenticated ?
                                        /*
                                        Button outline changed to <a> button (more visible)
                                        <Button outline onClick={this.toggleModal}>
                                            <span className="fa fa-sign-in fa-lg"></span> Login
                                            {this.props.auth.isFetching ?
                                                <span className="fa fa-spinner fa-pulse fa-fw"></span>
                                                : null
                                            }
                                        </Button>*/
                                        <span class="navbar-text">
                                            <a onClick={this.toggleModal} id="loginButton" role="button">
                                            <span className="fa fa-sign-in fa-lg"></span> Login</a>
                                            {this.props.auth.isFetching ?
                                                <span className="fa fa-spinner fa-pulse fa-fw"></span>
                                                : null
                                            }
                                        </span>    
                                        :
                                        /*<div>
                                        <div className="navbar-text mr-3">{this.props.auth.user.username}</div>
                                        <Button outline onClick={this.handleLogout}>
                                            <span className="fa fa-sign-out fa-lg"></span> Logout
                                            {this.props.auth.isFetching ?
                                                <span className="fa fa-spinner fa-pulse fa-fw"></span>
                                                : null
                                            }
                                        </Button>
                                        </div>*/
                                        /*
                                        <div>
                                            <div className="navbar-text mr-3">{this.props.auth.user.username}</div>
                                            <a onClick={this.handleLogout} id="loginButton" role="button">
                                            <span className="fa fa-sign-out fa-lg"></span> Logout</a>
                                            {this.props.auth.isFetching ?
                                                <span className="fa fa-spinner fa-pulse fa-fw"></span>
                                                : null
                                            }
                                           
                                        </div> */
                                        <div>
                                            <DropdownMenuComponent auth={this.props.auth} handleLogout={this.handleLogout}  user_data={this.props.user_data}  />
                                        </div>
                                        
                                    }

                                </NavItem>
                            </Nav>							
						</Collapse>
					</div>
				</Navbar>

                <Modal isOpen={this.state.isModalOpen} toggle={this.toggleModal}>
                    <ModalHeader toggle={this.toggleModal}>
                        <Nav tabs>
                            <NavItem className="userNav"> 
                                <NavLink
                                    className={classnames({ active: this.state.activeTab === '1' })}
                                    onClick={() => { this.toggleTab('1'); }}  to="/"
                                >
                                    Login        
                                </NavLink>
                            </NavItem>
                            <NavItem className="userNav">
                                <NavLink
                                    className={classnames({ active: this.state.activeTab === '2' })}
                                    onClick={() => { this.toggleTab('2'); }}  to="/"
                                >
                                    Sign up  
                                </NavLink>
                            </NavItem>
                        </Nav>
                    </ModalHeader>
                    <TabContent activeTab={this.state.activeTab}>
                        <TabPane tabId="1">
                            { this.state.activeTab == 1 ? 
                                <ModalBody>
                                    <Form onSubmit={this.handleLogin}>
                                        <FormGroup>
                                            <Label htmlFor="username">Username</Label>
                                            <Input type="text" id="username" name="username"
                                                innerRef={(input) => this.username = input} />
                                        </FormGroup>
                                        <FormGroup>
                                            <Label htmlFor="password">Password</Label>
                                            <Input type="password" id="password" name="password"
                                                innerRef={(input) => this.password = input}  />
                                        </FormGroup>
                                        <FormGroup check>
                                            <Label check>
                                                <Input type="checkbox" name="remember"
                                                innerRef={(input) => this.remember = input}  />
                                                Remember me
                                            </Label>
                                        </FormGroup>
                                        <Button type="submit" value="submit" color="secondary">Login</Button>
                                    </Form>
                                </ModalBody>
                            : null 
                            
                            }
                        </TabPane>
                        <TabPane tabId="2">
                            { this.state.activeTab == 2 ? 
                            
                                <ModalBody>
                                    <Form onSubmit={this.handleRegister}>
                                        <FormGroup>
                                            <Label htmlFor="username">Username</Label>
                                            <Input type="text" id="username" name="username"
                                                innerRef={(input) => this.username = input} />
                                        </FormGroup>
                                        <FormGroup>
                                            <Label htmlFor="first_name">First name</Label>
                                            <Input type="text" id="first_name" name="first_name"
                                                innerRef={(input) => this.first_name = input} />
                                        </FormGroup>
                                        <FormGroup>
                                            <Label htmlFor="last_name">Last name</Label>
                                            <Input type="text" id="last_name" name="last_name"
                                                innerRef={(input) => this.last_name = input} />
                                        </FormGroup>
                                        <FormGroup>
                                            <Label htmlFor="email">Email address</Label>
                                            <Input type="email" id="email" name="email"
                                                innerRef={(input) => this.email = input} />
                                        </FormGroup>
                                        <FormGroup>
                                            <Label htmlFor="password">Password</Label>
                                            <Input type="password" id="password" name="password"
                                                innerRef={(input) => this.password = input}  />
                                        </FormGroup>
                                        <FormGroup>
                                            <Label htmlFor="profile_image">Profile image</Label>
                                            <Input type="file" id="profile_image" name="profile_image"
                                                  onChange={this.handleImageChange} />
                                        </FormGroup>
                                        <FormGroup check>
                                            <Label check>
                                                <Input type="checkbox" name="remember"
                                                innerRef={(input) => this.remember = input}  />
                                                Remember me
                                            </Label>
                                        </FormGroup>
                                        <Button type="submit" value="submit" color="secondary">Sign up</Button>
                                    </Form>
                                </ModalBody>
                            : null }
                        </TabPane>
                    </TabContent>
                </Modal>				
			</>
		);
	}
}

export default Header;