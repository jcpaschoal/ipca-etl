from etl import create_report_job, transform_mocked_data, generate_mocked_data
import os

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "input")
    output_path = os.path.join(current_dir, "output")

    user_data = generate_mocked_data.generate_user_data(500)
    logs_data = generate_mocked_data.generate_log_data(user_data, 20000)

    generate_mocked_data.save_user_to_csv(user_data, "user.csv", path=input_path)
    generate_mocked_data.save_log_to_csv(logs_data, "event.csv", path=input_path)

    user_csv = os.path.join(input_path, "user.csv")
    event_csv = os.path.join(input_path, "event.csv")

    transform_mocked_data.transform_logs_csv(event_csv, "event.xlsx", path=output_path)
    transform_mocked_data.transform_users_csv(user_csv, "user.xlsx", path=output_path)

    user_xlsx = os.path.join(output_path, "user.xlsx")
    event_xlsx = os.path.join(output_path, "event.xlsx")

    transform_mocked_data.aggregate_user_logs(user_xlsx, event_xlsx, output_xls="info.xlsx", path=output_path)

    user_xlsx = os.path.join(output_path, "user.xlsx")
    event_xlsx = os.path.join(output_path, "event.xlsx")
    create_report_job.generate_report(user_xlsx, event_xlsx, "report.pdf")
