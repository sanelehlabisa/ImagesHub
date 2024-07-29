from tests import sign_in, get_users_data, post_image_data, get_images_data, serve_image, get_requests_data, post_request_data, update_request_data, get_image_data, get_user_data, get_request_data


def main():
    sign_in.test_sign_in(1)
    get_users_data.test_get_users_data(2)
    post_image_data.test_post_image_data(3)
    get_images_data.test_get_images_data(4)
    serve_image.test_serve_image(5)
    get_requests_data.test_get_requests_data(6)
    post_request_data.test_post_request_data(7)
    update_request_data.test_update_request_data(8)
    get_image_data.test_get_image_data(9)
    get_user_data.test_get_user_data(10)
    get_request_data.test_get_request_data(11)

if __name__ == "__main__":
    main()