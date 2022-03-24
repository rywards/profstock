function signInPage() {

    return(
        <div className="SignInPage">
        <h1>Sign In</h1>

        <form onSubmit={}>
            <label>
                Username:
                <input type="text" name="username" />
            </label>
            <label>
                Password:
                <input secureTextEntry="true" type="text" name="pw" />
            </label>
            <button type="submit">Sign In</button>
        </form>
        </div>

    );
} 

export default signInPage;