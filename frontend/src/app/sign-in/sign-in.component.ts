import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../user.service';
import { User } from '../user';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})

export class SignInComponent {
  signInForm: FormGroup = new FormGroup({});

  emailRegex: string = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$";

  constructor(private router: Router, private userService: UserService) {}

  ngOnInit(): void {
    this.signInForm = new FormGroup({
      email: new FormControl("", [
        Validators.required, 
        Validators.pattern(this.emailRegex)
      ])
    });
  }

  get email() {
    return this.signInForm.get('email');
  }

  signIn(): void {
    this.userService.signIn(this.email?.value).subscribe({
      next: (user: User) => {
        this.userService.setUser(user);
        let routerUrl: string = user.type == 0 ? "/guest/browse-images" : "/administrator/browse-requests";
        this.router.navigate([routerUrl]);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  signInWithGoogle(): void {

    this.userService.authorizeWithGoogle().subscribe({
      next: (res) => {
        console.log(res);
        // this.si
      },
      error: err => console.log(err)
  });


    this.userService.authorizeWithGoogle().subscribe({
      next: (user: User) => {
        this.userService.setUser(user);
        let routerUrl: string = user.type == 0 ? "/guest/browse-images" : "/administrator/browse-requests";
        this.router.navigate([routerUrl]);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }
}
