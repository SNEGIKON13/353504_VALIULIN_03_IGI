import * as ActionTypes from './ActionTypes';
import { baseUrlApiRest, apiUrl } from '../shared/baseUrl';

/* Request to Django Rest framework and show error or proceed to dispatch the data  */
export const fetchGenres = () => (dispatch) => {

    dispatch(genresLoading(true));

    return fetch(baseUrlApiRest + apiUrl + 'genres')
		.then(response => {
		  if (response.ok) {
        return response;
      } else {
        var error = new Error('Error ' + response.status + ': ' + response.statusText);
        error.response = response;
        throw error;
      }
		})
		.then(response => response.json())
    .then(genres => dispatch(addGenres(genres)))
    .catch(error => dispatch(genresFailed(error.message)));
}

/* Call action type from genre reducer */
export const genresLoading = () => ({
    type: ActionTypes.GENRES_LOADING
});

/* Call action type from genre reducer */
export const genresFailed = (errmess) => ({
    type: ActionTypes.GENRES_FAILED,
    payload: errmess
});

/* Call action type from genre reducer */
export const addGenres = (genres) => ({
    type: ActionTypes.ADD_GENRES,
    payload: genres
});

/* Request to Django Rest framework and show error or proceed to dispatch the data  */
export const fetchPosts = () => (dispatch) => {

  dispatch(postsLoading(true));

  return fetch(baseUrlApiRest + apiUrl + 'posts')
  .then(response => {
    if (response.ok) {
      return response;
    } else {
      var error = new Error('Error ' + response.status + ': ' + response.statusText);
      error.response = response;
      throw error;
    }
  })
  .then(response => response.json())
  .then(posts => dispatch(addPosts(posts)))
  .catch(error => dispatch(postsFailed(error.message)));
}

/* Call action type from post reducer */
export const postsLoading = () => ({
  type: ActionTypes.POSTS_LOADING
});

/* Call action type from post reducer */
export const postsFailed = (errmess) => ({
  type: ActionTypes.POSTS_FAILED,
  payload: errmess
});

/* Call action type from post reducer */
export const addPosts = (posts) => ({
  type: ActionTypes.ADD_POSTS,
  payload: posts
});


/* Request to Django Rest framework and show error or proceed to dispatch the data  */
export const fetchFeaturedPosts = () => (dispatch) => {

  dispatch(featuredpostsLoading(true));

  return fetch(baseUrlApiRest + apiUrl + 'featured_posts')
  .then(response => {
    if (response.ok) {
      return response;
    } else {
      var error = new Error('Error ' + response.status + ': ' + response.statusText);
      error.response = response;
      throw error;
    }
  })
  .then(response => response.json())
  .then(featuredposts => dispatch(addFeaturedPosts(featuredposts)))
  .catch(error => dispatch(featuredpostsFailed(error.message)));
}

/* Call action type from post reducer */
export const featuredpostsLoading = () => ({
  type: ActionTypes.FEATUREDPOSTS_LOADING
});

/* Call action type from post reducer */
export const featuredpostsFailed = (errmess) => ({
  type: ActionTypes.FEATUREDPOSTS_FAILED,
  payload: errmess
});

/* Call action type from post reducer */
export const addFeaturedPosts = (featuredposts) => ({
  type: ActionTypes.ADD_FEATUREDPOSTS,
  payload: featuredposts
});

/* Request to Django Rest framework and show error or proceed to dispatch the data  */
export const fetchComments = () => (dispatch) => {

  dispatch(commentsLoading(true));

  return fetch(baseUrlApiRest + apiUrl + 'comments')
  .then(response => {
    if (response.ok) {
      return response;
    } else {
      var error = new Error('Error ' + response.status + ': ' + response.statusText);
      error.response = response;
      throw error;
    }
  })
  .then(response => response.json())
  .then(comments => dispatch(addComments(comments)))
  .catch(error => dispatch(commentsFailed(error.message)));
}

/* Call action type from comment reducer */
export const commentsLoading = () => ({
  type: ActionTypes.COMMENTS_LOADING
});

/* Call action type from comment reducer */
export const commentsFailed = (errmess) => ({
  type: ActionTypes.COMMENTS_FAILED,
  payload: errmess
});

/* Call action type from comment reducer to add all comments */
export const addComments = (comments) => ({
  type: ActionTypes.ADD_COMMENTS,
  payload: comments
});

/* Call action type from comment reducer to add one comment */
export const addComment = (comment) => ({
  type: ActionTypes.ADD_COMMENT,
  payload: comment
});

/**
 * Send post request to save comment
 */
export const postComment = (post, content) => (dispatch) => {
  const author = localStorage.getItem('user_id');
  const newComment = {
    post: post,
    author: author,
    content: content
  }
  const bearer = 'Bearer ' + localStorage.getItem('token');
  //console.log("comment value: "+ JSON.stringify(newComment))
  return fetch(baseUrlApiRest + apiUrl + 'comments', {
    method: "POST",
    body: JSON.stringify(newComment),
    headers: {
      "Content-Type": "application/json",
      'Authorization': bearer
    },
    credentials: "same-origin"
  })
  .then(response => {
      if (response.ok) {
        return response;
      } else {
        var error = new Error('Error ' + response.status + ': ' + response.statusText);
        error.response = response;
        throw error;
      }
    },
    error => {
          throw error;
    })
  .then(response => response.json())
  //.then(response => dispatch(addComment(response)))
  .then(response => { console.log('Comment', response); /*alert('Thank you for your comment!\n'+JSON.stringify(response));*/ })
  .catch(error =>  { console.log('comment', error.message); /*alert('Your comment could not be posted\nError: '+error.message);*/ });
};

/**
 * Send rate request to save Post rating
 */
 export const ratePost = (post, rating) => (dispatch) => {

  const author = localStorage.getItem('user_id');

  //var string_rating = (rating).toString();;

  const newRating = {
    post: post,
    author: author,
    rating: rating
  }

  const bearer = 'Bearer ' + localStorage.getItem('token');

  alert("rating value: "+ JSON.stringify(newRating));
  
  return fetch(baseUrlApiRest + apiUrl + 'rate_posts', {
    method: "POST",
    body: JSON.stringify(newRating),
    headers: {
      "Content-Type": "application/json",
      'Authorization': bearer
    },
    credentials: "same-origin"
  })
  .then(response => {
      if (response.ok) {
        return response;
      } else {
        var error = new Error('Error ' + response.status + ': ' + response.statusText);
        error.response = response;
        throw error;
      }
    },
    error => {
          throw error;
    })
  .then(response => response.json())
  .then(response => { console.log('Rating', response); alert('Thank you for rating this post!\n'+JSON.stringify(response)); })
  .catch(error =>  { console.log('Rating', error.message); alert('Your rating could not be saved\nError: '+error.message); });
};

/**
 ***********************************************
 * Login/Logout user JSON web token requests
 ***********************************************
 */

export const requestLogin = (creds) => {
  return {
      type: ActionTypes.LOGIN_REQUEST,
      creds
  }
}

export const receiveLogin = (response) => {
  return {
      type: ActionTypes.LOGIN_SUCCESS,
      token: response.token
  }
}

export const loginError = (message) => {
  return {
      type: ActionTypes.LOGIN_FAILURE,
      message
  }
}

export const loginUser = (creds) => (dispatch) => {
  // We dispatch requestLogin to kickoff the call to the API
  dispatch(requestLogin(creds))

  return fetch(baseUrlApiRest + apiUrl +  'token/', {
      method: 'POST',
      headers: { 
          'Content-Type':'application/json' 
      },
      body: JSON.stringify(creds)
  })
  .then(response => {
      if (response.ok) {
          return response;
      } else {
          var error = new Error('Error ' + response.status + ': ' + response.statusText);
          error.response = response;
          throw error;
      }
      },
      error => {
          throw error;
      })
  .then(response => response.json())
  .then(response => {
      if (response.access) {
          // If login was successful, set the token in local storage
          localStorage.setItem('token', response.access);

          // Save user id in local storage to make post requests with id (comments)
          localStorage.setItem('user_id', response.user_id);
          localStorage.setItem('creds', JSON.stringify(creds));
          // Dispatch the success action
          dispatch(receiveLogin(response));
          // Get user data after login
          dispatch(fetchUserData());
      }
      else {
          var error = new Error('Error ' + response.status);
          error.response = response;
          throw error;
      }
  })
  .catch(error => { console.log('Login user', error.message); alert('User could not be authenticated\nError: '+error.message);dispatch(loginError(error.message)); }   ) 
};

export const requestLogout = () => {
  return {
    type: ActionTypes.LOGOUT_REQUEST
  }
}

export const receiveLogout = () => {
  return {
    type: ActionTypes.LOGOUT_SUCCESS
  }
}

// Logs the user out
export const logoutUser = () => (dispatch) => {
  dispatch(requestLogout())
  localStorage.removeItem('token');
  localStorage.removeItem('creds');
  dispatch(receiveLogout())
}

/**
 * Register user
 */
export const registerUser = (dataUser) => (dispatch) => {
  
  // Link set formdata to send post request 
  // https://stackoverflow.com/questions/48284011/how-to-post-image-with-fetch
  //console.log(dataUser.profile_image);

  let form_data = new FormData();
  form_data.append('username', dataUser.username);
  form_data.append('email', dataUser.email);
  form_data.append('first_name', dataUser.first_name);
  form_data.append('last_name', dataUser.last_name);
  form_data.append('password', dataUser.password);
  form_data.append('profile_image', dataUser.profile_image);
  
  //console.log(dataUser.profile_image);
  return fetch(baseUrlApiRest + apiUrl + 'users', {
      method: "POST",
      //body: JSON.stringify(dataUser),
      body: form_data,
      /*headers: {
        //"Content-Type": "application/json"
        "Content-Type": "multipart/form-data",
      },*/
      credentials: "same-origin"
  })
  .then(response => {
      if (response.ok) {
        return response;
      } else {
        var error = new Error('Error ' + response.status + ': ' + response.statusText);
        error.response = response;
        throw error;
      }
    },
    error => {
          throw error;
    })
  .then(response => response.json())
  .then(response => { console.log('Register user', response); alert('Thank you for your registration!\n'+JSON.stringify(response)); })
  .catch(error =>  { console.log('Register user', error.message); alert('User could not be registered\nError: '+error.message); });
};

/**
 * Register user
 */
 export const updateUser = (dataUser) => (dispatch) => {
  
  // Link set formdata to send post request 
  // https://stackoverflow.com/questions/48284011/how-to-post-image-with-fetch
  
  const user_id = localStorage.getItem('user_id');

  const bearer = 'Bearer ' + localStorage.getItem('token');

  return fetch(baseUrlApiRest + apiUrl + 'update_user/' + user_id + '/', {
      method: "PUT",
      body: JSON.stringify(dataUser),
      headers: {
        "Content-Type": "application/json",
        'Authorization': bearer
      },
      credentials: "same-origin"
  })
  .then(response => {
      if (response.ok) {
        return response;
      } else {
        var error = new Error('Error ' + response.status + ': ' + response.statusText);
        error.response = response;
        throw error;
      }
    },
    error => {
          throw error;
    })
  .then(response => response.json())
  .then(response => { console.log('Update user', response); alert('Thank you for your updating!\n'+JSON.stringify(response)); })
  .catch(error =>  { console.log('Update user', error.message); alert('User could not be updated\nError: '+error.message); });
};

/* Request to Django Rest framework and show error or proceed to dispatch the data  */
export const fetchUserData = () => (dispatch) => {

  dispatch(UserDataLoading(true));

  const user_id = localStorage.getItem('user_id');

  const bearer = 'Bearer ' + localStorage.getItem('token');

  return fetch(baseUrlApiRest + apiUrl + 'update_user/' + user_id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        'Authorization': bearer
      },
      credentials: "same-origin"
  })
  .then(response => {
    if (response.ok) {
      return response;
    } else {
      var error = new Error('Error ' + response.status + ': ' + response.statusText);
      error.response = response;
      throw error;
    }
  })
  .then(response => response.json())
  .then(user_data => dispatch(addUserData(user_data)))
  .catch(error => dispatch(UserDataFailed(error.message)));
}

/* Call action type from genre reducer */
export const UserDataLoading = () => ({
    type: ActionTypes.USER_DATA_LOADING
});

/* Call action type from genre reducer */
export const UserDataFailed = (errmess) => ({
    type: ActionTypes.USER_DATA_FAILED,
    payload: errmess
});

/* Call action type from comment reducer to add one comment */
export const addUserData = (user_data) => ({
  type: ActionTypes.ADD_USER_DATA,
  payload: user_data
});


/* Request to Django Rest framework and show error or proceed to dispatch the data  */
export const fetchProfileImages = () => (dispatch) => {

  dispatch(ProfileImagesLoading(true));

  return fetch(baseUrlApiRest + apiUrl + 'profile_images')
  .then(response => {
    if (response.ok) {
      return response;
    } else {
      var error = new Error('Error ' + response.status + ': ' + response.statusText);
      error.response = response;
      throw error;
    }
  })
  .then(response => response.json())
  .then(profile_images => dispatch(addProfileImages(profile_images)))
  .catch(error => dispatch(ProfileImagesFailed(error.message)));
}

/* Call action type from genre reducer */
export const ProfileImagesLoading = () => ({
    type: ActionTypes.PROFILE_IMAGES_LOADING
});

/* Call action type from genre reducer */
export const ProfileImagesFailed = (errmess) => ({
    type: ActionTypes.PROFILE_IMAGES_FAILED,
    payload: errmess
});

/* Call action type from comment reducer to add one comment */
export const addProfileImages = (profile_images) => ({
  type: ActionTypes.ADD_PROFILE_IMAGES,
  payload: profile_images
});