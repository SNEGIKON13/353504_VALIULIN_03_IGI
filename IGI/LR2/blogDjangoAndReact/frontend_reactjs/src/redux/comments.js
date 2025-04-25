import * as ActionTypes from './ActionTypes';

/* Set reducer to handle redux state */
export const Comments = (state = { 
    isLoading: true,
    errMess: null,
    comments:[]}, action) => {
    switch (action.type) {
        case ActionTypes.ADD_COMMENTS:
            return {...state, isLoading: false, errMess: null, comments: action.payload};

        case ActionTypes.COMMENTS_LOADING:
            return {...state, isLoading: true, errMess: null, comments: []}

        case ActionTypes.COMMENTS_FAILED:
            return {...state, isLoading: false, errMess: action.payload};

        case ActionTypes.ADD_COMMENT:
            var comment = action.payload;
            return {...state, comments: state.comments.concat(comment)};

        default:
            return state;
    }
};