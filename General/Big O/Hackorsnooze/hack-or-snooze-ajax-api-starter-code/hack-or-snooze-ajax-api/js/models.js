"use strict";

const BASE_URL = "https://hack-or-snooze-v3.herokuapp.com";

/******************************************************************************
 * Story: a single story in the system
 */

class Story {

  /** Make instance of Story from data object about story:
   *   - {title, author, url, username, storyId, createdAt}
   */

  constructor({ storyId, title, author, url, username, createdAt }) {
    this.storyId = storyId;
    this.title = title;
    this.author = author;
    this.url = url;
    this.username = username;
    this.createdAt = createdAt;
  }

  /** Parses hostname out of URL and returns it. */

  getHostName() {
    // UNIMPLEMENTED: complete this function!
    return "hostname.com";
  }
}


/******************************************************************************
 * List of Story instances: used by UI to show story lists in DOM.
 */

class StoryList {
  constructor(stories) {
    this.stories = stories;
  }

  /** Generate a new StoryList. It:
   *
   *  - calls the API
   *  - builds an array of Story instances
   *  - makes a single StoryList instance out of that
   *  - returns the StoryList instance.
   */

  

  static async getStories() {
    // Note presence of `static` keyword: this indicates that getStories is
    //  **not** an instance method. Rather, it is a method that is called on the
    //  class directly. Why doesn't it make sense for getStories to be an
    //  instance method?

    // query the /stories endpoint (no auth required)
    const response = await axios({
      url: `${BASE_URL}/stories`,
      method: "GET",
    });

    // turn plain old story objects from API into instances of Story class
    const stories = response.data.stories.map(story => new Story(story));

    // build an instance of our own class using the new array of stories
    return new StoryList(stories);
  }

  /** Adds story data to API, makes a Story instance, adds it to story list.
   * - user - the current instance of User who will post the story
   * - obj of {title, author, url}
   *
   * Returns the new Story instance
   */

  async addStory(user, newStory) {
    const token = user.loginToken; 

    // Make a POST request to the API to add the story
    const response = await axios.post(`https://hack-or-snooze-v3.herokuapp.com/stories`, {
      token: token,
      story: newStory
    });

    // Create a new Story instance
    const { storyId, title, author, url, username, createdAt } = response.data.story;
    const story = new Story({ storyId, title, author, url, username, createdAt });

    // Add the new story to the story list
    this.stories.push(story);

    return story; // Return the Story instance
  }
}


/******************************************************************************
 * User: a user in the system (only used to represent the current user)
 */

class User {
  /** Make user instance from obj of user data and a token:
   *   - {username, name, createdAt, favorites[], ownStories[]}
   *   - token
   */

  constructor({
                username,
                name,
                createdAt,
                favorites = [],
                ownStories = []
              },
              token) {
    this.username = username;
    this.name = name;
    this.createdAt = createdAt;

    // instantiate Story instances for the user's favorites and ownStories
    this.favorites = favorites.map(s => new Story(s));
    this.ownStories = ownStories.map(s => new Story(s));

    // store the login token on the user so it's easy to find for API calls.
    this.loginToken = token;
  }

  /** Register new user in API, make User instance & return it.
   *
   * - username: a new username
   * - password: a new password
   * - name: the user's full name
   */

  static async signup(username, password, name) {
    const response = await axios({
      url: `${BASE_URL}/signup`,
      method: "POST",
      data: { user: { username, password, name } },
    });

    let { user } = response.data

    return new User(
      {
        username: user.username,
        name: user.name,
        createdAt: user.createdAt,
        favorites: user.favorites,
        ownStories: user.stories
      },
      response.data.token
    );
  }

  /** Login in user with API, make User instance & return it.

   * - username: an existing user's username
   * - password: an existing user's password
   */

  static async login(username, password) {
    const response = await axios({
      url: `${BASE_URL}/login`,
      method: "POST",
      data: { user: { username, password } },
    });

    let { user } = response.data;

    return new User(
      {
        username: user.username,
        name: user.name,
        createdAt: user.createdAt,
        favorites: user.favorites,
        ownStories: user.stories
      },
      response.data.token
    );
  }

  /** When we already have credentials (token & username) for a user,
   *   we can log them in automatically. This function does that.
   */

  static async loginViaStoredCredentials(token, username) {
    try {
      const response = await axios({
        url: `${BASE_URL}/users/${username}`,
        method: "GET",
        params: { token },
      });

      let { user } = response.data;

      return new User(
        {
          username: user.username,
          name: user.name,
          createdAt: user.createdAt,
          favorites: user.favorites,
          ownStories: user.stories
        },
        token
      );
    } catch (err) {
      console.error("loginViaStoredCredentials failed", err);
      return null;
    }
  }

  /** Add a story to the user's list of favorite stories.
   * - storyId: the ID of the story to add to favorites
   */
async addFavorite(storyId) {
  // Make a POST request to add the story to favorites
  const response = await axios({
    url: `${BASE_URL}/users/${this.username}/favorites/${storyId}`,
    method: "POST",
    data: { token: this.loginToken },
  });

  // Update the user's favorites list
  this.favorites.push(storyId);
}

/** Remove a story from the user's list of favorite stories.
 * - storyId: the ID of the story to remove from favorites
 */
async removeFavorite(storyId) {
  // Make a DELETE request to remove the story from favorites
  const response = await axios({
    url: `${BASE_URL}/users/${this.username}/favorites/${storyId}`,
    method: "DELETE",
    data: { token: this.loginToken },
  });

  // Update the user's favorites list
  this.favorites = this.favorites.filter(id => id !== storyId);
}

/** Get a list of the user's favorite stories.
 * Returns an array of story IDs.
 */
async getFavoriteStories() {
  // Make a GET request to get the user's favorites
  const response = await axios({
    url: `${BASE_URL}/users/${this.username}`,
    method: "GET",
    params: { token: this.loginToken },
  });

  // Return the list of favorite story IDs
  return response.data.user.favorites;
}
/** Remove a story from the user's list of own stories and from the API.
   * - storyId: the ID of the story to remove
   */
async removeStory(storyId) {
  // Make a DELETE request to remove the story
  const response = await axios({
    url: `${BASE_URL}/stories/${storyId}`,
    method: "DELETE",
    data: { token: this.loginToken },
  });

  // Remove the story from the user's list of own stories
  this.ownStories = this.ownStories.filter(story => story.storyId !== storyId);
}
}
