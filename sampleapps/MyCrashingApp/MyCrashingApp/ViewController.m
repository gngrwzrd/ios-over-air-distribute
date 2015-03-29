//
//  ViewController.m
//  MyCrashingApp
//
//  Created by Aaron Smith on 3/28/15.
//  Copyright (c) 2015 gngrwzrd. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
	[super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning {
	[super didReceiveMemoryWarning];
	// Dispose of any resources that can be recreated.
}

- (IBAction) crash:(id)sender {
	NSArray * myArray = [NSArray array];
	id tmp = [myArray objectAtIndex:100];
}

@end
