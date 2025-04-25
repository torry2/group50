from flask import jsonify, redirect, url_for

def error_routes(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "404"}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "500"}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({"error": "unknown"}), 501

# we can define more specific errors as part of the main login (also add the error_page function for url_for)
'''
@app.route('/error/<int:error_code>')
    def error_page(error_code):
        return jsonify({"error": f"An error occurred: {error_code}"}), error_code
'''