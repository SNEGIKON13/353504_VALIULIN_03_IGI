import * as ActionTypes from './ActionTypes';

/* Set reducer to handle redux state */
export const FeaturedPosts = (state = { 
    isLoading: true,
    errMess: null,
    featuredposts:[]}, action) => {
    switch (action.type) {
        case ActionTypes.ADD_FEATUREDPOSTS:
            return {...state, isLoading: false, errMess: null, featuredposts: action.payload};

        case ActionTypes.FEATUREDPOSTS_LOADING:
            return {...state, isLoading: true, errMess: null, featuredposts: []}

        case ActionTypes.FEATUREDPOSTS_FAILED:
            return {...state, isLoading: false, errMess: action.payload};

        default:
            return state;
    }
};